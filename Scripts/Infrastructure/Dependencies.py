from Scripts.Application.UseCases.AddUserUseCase import AddUserUseCase
from Scripts.Application.UseCases.ChangeAiUseCase import ChangeAiUseCase
from Scripts.Application.UseCases.ChangeUserLanguageUseCase import ChangeUserLanguageUseCase
from Scripts.Application.UseCases.GetUserDataUseCase import GetUserDataUseCase
from Scripts.Application.UseCases.LoggingAccessPaymentUseCase import LoggingAccessPaymentUseCase
from Scripts.Application.UseCases.RecreateAiUseCase import RecreateAiUseCase
from Scripts.Application.UseCases.ReturnTextsUseCase import ReturnTextsUseCase
from Scripts.Application.UseCases.SendUserMessageUseCase import SendUserMessageUseCase
from Scripts.Infrastructure.Database import Database
from Scripts.Infrastructure.PostgresSQLDatabase.UserRequests import UserRequests
from Scripts.Infrastructure.Services.Logger import Logger
from Scripts.Infrastructure.TechData.Constants import Constants
from Scripts.Presentation.ClientHandlers.BaseHandlers import BaseHandlers
from Scripts.Presentation.ClientHandlers.ChangeLanguageHandlers import ChangeLanguageHandlers
from Scripts.Presentation.ClientHandlers.RecreateAiHandlers import RecreateAiHandlers
from Scripts.Presentation.ClientHandlers.ShopHandlers import ShopHandlers
from Scripts.Presentation.HandlersRegistrator import HandlersRegistrator


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
        self.constants = Constants()
        self.user_requests = UserRequests(db)

    def __initialize_handlers(self):
        self.shop_handlers = ShopHandlers(self.add_user_usecase,
                                 self.change_ai_usecase,
                                 self.change_user_language_usecase,
                                 self.recreate_ai_usecase,
                                 self.logging_acces_payment_usecase,
                                 self.return_texts_usecase,
                                 self.get_user_data_usecase,
                                 self.constants)
        self.change_language_handlers = ChangeLanguageHandlers(self.add_user_usecase,
                                 self.change_ai_usecase,
                                 self.change_user_language_usecase,
                                 self.recreate_ai_usecase,
                                 self.logging_acces_payment_usecase,
                                 self.return_texts_usecase,
                                 self.get_user_data_usecase)
        self.base_handlers = BaseHandlers(self.add_user_usecase,
                                 self.change_ai_usecase,
                                 self.change_user_language_usecase,
                                 self.recreate_ai_usecase,
                                 self.logging_acces_payment_usecase,
                                 self.return_texts_usecase,
                                 self.get_user_data_usecase,
                                 self.send_user_message_usecase)
        self.recreate_ai_handlers = RecreateAiHandlers(self.add_user_usecase,
                                 self.change_ai_usecase,
                                 self.change_user_language_usecase,
                                 self.recreate_ai_usecase,
                                 self.logging_acces_payment_usecase,
                                 self.return_texts_usecase,
                                 self.get_user_data_usecase)
        self.handler_registrator = HandlersRegistrator(self.constants,
                                                       self.base_handlers,
                                                       self.change_language_handlers,
                                                       self.recreate_ai_handlers,
                                                       self.shop_handlers)


    def __initialize_usecases(self):
        self.add_user_usecase = AddUserUseCase(self.user_requests)
        self.change_ai_usecase = ChangeAiUseCase(self.user_requests)
        self.change_user_language_usecase = ChangeUserLanguageUseCase(self.user_requests)
        self.recreate_ai_usecase = RecreateAiUseCase(self.user_requests)
        self.logging_acces_payment_usecase = LoggingAccessPaymentUseCase(self.logger)
        self.return_texts_usecase = ReturnTextsUseCase(self.user_requests)
        self.get_user_data_usecase = GetUserDataUseCase(self.user_requests)
        self.send_user_message_usecase = SendUserMessageUseCase(self.user_requests, self.constants)