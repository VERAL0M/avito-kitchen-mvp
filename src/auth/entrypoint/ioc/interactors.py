from dishka import Provider, Scope, provide

from auth.application.interactors.create_order import CreateOrderInteractor
from auth.application.interactors.list_order import StatusFilterOrderInteractor
from auth.application.interactors.find_order import FindOrderInteractor
from auth.application.interactors.cancel_order import CancelOrderInteractor
from auth.application.interactors.confirm_order import ConfirmOrderInteractor


class InteractorProvider(Provider):
    scope = Scope.REQUEST

    create_order = provide(CreateOrderInteractor)
    list_order = provide( StatusFilterOrderInteractor)
    find_order = provide(FindOrderInteractor)
    cancel_order = provide(CancelOrderInteractor)
    confirm_order = provide(ConfirmOrderInteractor)

