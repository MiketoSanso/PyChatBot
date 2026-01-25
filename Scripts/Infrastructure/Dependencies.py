from Scripts.Application.UseCases.AddUserUseCase import AddUserUseCase
from Scripts.Application.UseCases.ChangeAiUseCase import ChangeAiUseCase
from Scripts.Application.UseCases.ChangeUserLanguageUseCase import ChangeUserLanguageUseCase
from Scripts.Application.UseCases.LoggingAccessPaymentUseCase import LoggingAccessPaymentUseCase
from Scripts.Application.UseCases.RecreateAiUseCase import RecreateAiUseCase
from Scripts.Application.UseCases.ReturnTextsUseCase import ReturnTextsUseCase
from Scripts.Infrastructure.Database import Database
from Scripts.Infrastructure.PostgresSQLDatabase.UserRequests import UserRequests
from Scripts.Infrastructure.Services.Logger import Logger
from Scripts.Presentation.ClientHandlers.Handlers import Handlers


class Dependencies:
    def __init__(self):
        self.__initialize_services_and_domain()
        self.__initialize_requests()
        self.__initialize_usecases()
        self.__initialize_handlers()

    def __initialize_services_and_domain(self):

        self.logger = Logger()

    def __initialize_requests(self):
        db = Database()
        self.user_requests = UserRequests(db)

    def __initialize_handlers(self):
        self.handlers = Handlers(self.add_user_usecase,
                                 self.change_ai_usecase,
                                 self.change_user_language_usecase,
                                 self.recreate_ai_usecase,
                                 self.logging_acces_payment_usecase,
                                 self.return_texts_usecase)

    def __initialize_usecases(self):
        self.add_user_usecase = AddUserUseCase(self.user_requests)
        self.change_ai_usecase = ChangeAiUseCase(self.user_requests)
        self.change_user_language_usecase = ChangeUserLanguageUseCase(self.user_requests)
        self.recreate_ai_usecase = RecreateAiUseCase(self.user_requests)
        self.logging_acces_payment_usecase = LoggingAccessPaymentUseCase(self.logger)
        self.return_texts_usecase = ReturnTextsUseCase(self.user_requests)