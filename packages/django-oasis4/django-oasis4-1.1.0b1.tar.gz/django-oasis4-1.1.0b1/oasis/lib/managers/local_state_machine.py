# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         8/03/23 9:01
# Project:      CFHL Transactional Backend
# Module Name:  local_state_machine
# Description:
# ****************************************************************
from typing import Any
from zibanu.django.db import models


class StateMachine(models.Manager):
    def get_next_state(self) -> Any:
        pass
