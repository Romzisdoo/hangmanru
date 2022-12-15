from flask_login import UserMixin

class UserLogin(UserMixin):
# Naudojamas sukuriant vartoja dekoratoriuje load_user
    def fromDB(self, user_id, db):
        self.__user = db.get_user(user_id)
        return self

# Iskvieciama si funkcija kai vartotojas praeina autorizavima, perduodama klasei UserLogin
    def create(self, user):
        self.__user = user
        return self

# # tikrinama ar vartojas autorizuotas
#     def is_autenhenticated(self): 
#         return True

# # Tikrinama ar vartotojas aktyvus, paprastinant laikom, kad visada aktyvus
#     def is_active(self):
#         return True

# # Jei neautorizuotas True, jei neautorizuotas False 
#     def is_anonymous(self):
#         return False
# Butinas metodas. Grazina identifikatoriu per kuri nustatome konkretu vartotoja (butinai stringu)
    def get_id(self):
        return str(self.__user['id'])