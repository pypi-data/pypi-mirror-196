# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         6/03/23 16:24
# Project:      CFHL Transactional Backend
# Module Name:  offer_state_machine
# Description:
# ****************************************************************
from django.db import DatabaseError
from django.utils.translation import gettext_lazy as _
from oasis.models import Operation
from oasis.models import StateMachine


class OfferStateMachine:
    def __init__(self, offer, operation):
        self.__offer = offer
        self.__operation = operation
        self.__from_status = offer.status

    def run(self) -> None:
        oasis_state = self.__operation.state
        oasis_status = self.__operation.status
        machine_qs = StateMachine.objects.filter(from_state__exact=self.__from_status, oasis_state__exact=oasis_state,
                                                 oasis_status__exact=oasis_status, update_oasis__exact=False)
        state = machine_qs.first()
        if state is not None:
            self.__offer.status = state.state
            # Change kg received
            if self.__offer.kg_received != self.__operation.quantity:
                self.__offer.kg_received = self.__operation.quantity

            if state.is_changed:
                # Change kg offered
                if self.__offer.kg_offered != self.__operation.otherif:
                    self.__offer.kg_offered = self.__operation.otherif
                # Change delivery date
                if self.__offer.delivery_Date != self.__operation.finaldate:
                    self.__offer.delivery_date = self.__operation.finaldate

            self.__offer.save()

    def set(self, new_state: int) -> None:
        state = StateMachine.objects.filter(from_state__exact=self.__offer.status, state__exact=new_state,
                                            update_oasis__exact=True).first()

        if state is not None:
            if Operation.objects.update_status(location_id=self.__operation.locationid, document_id=self.__operation.documentid, number_id=self.__operation.numberid, state=state.oasis_state, status=state.oasis_status):
                self.__offer.status = new_state
                self.__offer.save()
            else:
                raise DatabaseError(_("Error updating operation record"))
