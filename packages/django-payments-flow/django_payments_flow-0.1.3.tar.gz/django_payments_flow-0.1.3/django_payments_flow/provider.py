from typing import Any, Optional

from django.http import JsonResponse
from payments import PaymentError, PaymentStatus, RedirectNeeded
from payments.core import BasicProvider, get_base_url
from payments.forms import PaymentForm as BasePaymentForm
from pyflowcl import Payment as FlowPayment
from pyflowcl.Clients import ApiClient


class FlowProvider(BasicProvider):
    """
    FlowProvider es una clase que proporciona integración con Flow para procesar pagos.
    Inicializa una instancia de FlowProvider con el key y el secreto de Flow.

    Args:
        key (str): ID de receptor de Khipu.
        secret (str): Secreto de Khipu.
        medio (int | None): Versión de la API de notificaciones a utilizar (Valor por defecto: 9).
        **kwargs: Argumentos adicionales.
    """

    form_class = BasePaymentForm
    endpoint: str
    key: str = None
    secret: str = None
    medio: int = 9
    _client: Any = None

    def __init__(self, endpoint: str, key: str, secret: str, medio: int, **kwargs):
        super().__init__(**kwargs)
        self.endpoint = endpoint
        self.key = key
        self.secret = secret
        self.medio = medio
        self._client = ApiClient(self.endpoint, self.key, self.secret)

    def get_form(self, payment, data: Optional[dict] = None) -> Any:
        """
        Genera el formulario de pago para redirigir a la página de pago de Khipu.

        Args:
            payment: Objeto de pago.
            data (dict | None): Datos del formulario (opcional).

        Returns:
            Any: Formulario de pago redirigido a la página de pago de Khipu.

        Raises:
            RedirectNeeded: Redirige a la página de pago de Khipu.

        """
        if not payment.transaction_id:
            datos_para_flow = {
                "commerceOrder": payment.token,
                "urlReturn": payment.get_success_url(),
                "urlConfirmation": f"{get_base_url()}{payment.get_process_url()}",
                "subject": payment.description,
                "amount": int(payment.total),
                "paymentMethod": self.medio,
                "currency": payment.currency,
            }

            if payment.billing_email:
                datos_para_flow.update({"email": payment.billing_email})

            datos_para_flow.update(**self._extra_data(payment.attrs))

            try:
                payment.attrs.datos_flow = datos_para_flow
                payment.save()
            except Exception as e:
                raise PaymentError(f"Ocurrió un error al guardar attrs.datos_flow: {e}")

            try:
                pago = FlowPayment.create(self._client, datos_para_flow)

            except Exception as pe:
                payment.change_status(PaymentStatus.ERROR, str(pe))
                raise PaymentError(pe)
            else:
                payment.transaction_id = pago.token
                payment.attrs.respuesta_flow = {"url": pago.url, "token": pago.token, "flowOrder": pago.flowOrder}
                payment.save()

            raise RedirectNeeded(f"{pago.url}?token={pago.token}")

    def process_data(self, payment, request) -> JsonResponse:
        """
        Procesa los datos del pago recibidos desde Khipu.

        Args:
            payment: Objeto de pago.
            request: Objeto de solicitud HTTP de Django.

        Returns:
            JsonResponse: Respuesta JSON que indica el procesamiento de los datos del pago.

        """
        return JsonResponse("process_data")

    def _extra_data(self, attrs) -> dict:
        if "datos_extra" not in attrs:
            return {}

        data = attrs.datos_extra
        if "commerceOrder" in data:
            del data["commerceOrder"]

        if "urlReturn" in data:
            del data["urlReturn"]

        if "urlConfirmation" in data:
            del data["urlConfirmation"]

        if "amount" in data:
            del data["amount"]

        if "subject" in data:
            del data["subject"]

        if "paymentMethod" in data:
            del data["paymentMethod"]

        if "currency" in data:
            del data["currency"]

        return data

    def refund(self, payment, amount: Optional[int] = None) -> int:
        """
        Realiza un reembolso del pago.

        Args:
            payment: Objeto de pago.
            amount (int | None): Monto a reembolsar (opcional).

        Returns:
            int: Monto reembolsado.

        Raises:
            PaymentError: Error al realizar el reembolso.

        """
        if payment.status != PaymentStatus.CONFIRMED:
            raise PaymentError("El pago debe estar confirmado para reversarse.")

        to_refund = amount or payment.total
        try:
            refund = self._client.payments.post_refunds(payment.transaction_id, to_refund)
        except Exception as pe:
            raise PaymentError(pe)
        else:
            payment.attrs.refund = refund
            payment.save()
            payment.change_status(PaymentStatus.REFUNDED)
            return to_refund

    def capture(self, payment, amount=None):
        """
        Captura el monto del pago.

        Args:
            payment: Objeto de pago.
            amount: Monto a capturar (no utilizado).

        Raises:
            NotImplementedError: Método no implementado.

        """
        raise NotImplementedError()

    def release(self, payment):
        """
        Libera el pago (no implementado).

        Args:
            payment: Objeto de pago.

        Raises:
            NotImplementedError: Método no implementado.

        """
        raise NotImplementedError()
