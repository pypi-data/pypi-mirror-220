# django-payments-flow

`Proyecto en desarrollo activo, no listo para produccion`

`django-payments-flow` es una variante de Django Payments que implementa la
creación, confirmación y expiración de pagos realizados a través de Flow. Este
módulo proporciona integración con la API de Flow para facilitar el
procesamiento y gestión de pagos en tu aplicación web Django.

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/7dc3c8d6fe844fdaa1de0cb86c242934)](https://app.codacy.com/gh/mariofix/django-payments-flow/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/7dc3c8d6fe844fdaa1de0cb86c242934)](https://app.codacy.com/gh/mariofix/django-payments-flow/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/mariofix/django-payments-flow/main.svg)](https://results.pre-commit.ci/latest/github/mariofix/django-payments-flow/main)
![PyPI](https://img.shields.io/pypi/v/django-payments-flow)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-payments-flow)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/django-payments-flow)
![PyPI - License](https://img.shields.io/pypi/l/django-payments-flow)
![PyPI - Status](https://img.shields.io/pypi/status/django-payments-flow)



## Introducción

`django-payments-flow` está diseñado para simplificar la integración de
pagos de Flow en tu proyecto Django Payments. Con este módulo, puedes crear y
gestionar pagos utilizando la pasarela de pago de Flow de manera sencilla.

Características principales:

- Crea y procesa pagos de forma segura con Flow.
- Recibe notificaciones de confirmación de pago.
- Maneja automáticamente la expiración y cancelación de pagos.

## Instalación

Puedes instalar django-payments-flow utilizando pip:

```shell
pip install django-payments-flow
```

O utilizando poetry:

```shell
poetry add django-payments-flow
```

## Configuración

La configuracion se realiza como una variante de Django Payments

```python
PAYMENT_VARIANTS = {
    "flow": ("django_payments_flow.FlowProvider", {
        "key": 1,
        "secret": "qwertyasdf0123456789",
    })
}
```

Puedes ver mas opciones de configuracion [en la documentacion](https://mariofix.github.io/django-payments-flow/uso/#variables-de-configuracion)

## Licencia

El código está bajo licencia MIT
