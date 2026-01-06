import os

# Order matters: top = highest authority
FOLDER_RULES = [
    ("data", "BACKEND"),
    ("domain", "BACKEND"),
    ("repository", "BACKEND"),
    ("dao", "DAO"),
    ("entity", "ENTITY"),
    ("db", "DATABASE"),
    ("database", "DATABASE"),
    ("usecase", "USECASE"),
    ("facade", "FACADE"),
    ("service", "SERVICE"),

    ("ui", "FRONTEND"),
    ("screen", "SCREEN"),
    ("viewmodel", "VIEWMODEL"),
    ("navigation", "NAVIGATION"),
    ("components", "COMPONENT"),
    ("dialog", "DIALOG"),
]

FILENAME_RULES = [
    ("ViewModel", "VIEWMODEL"),
    ("Screen", "SCREEN"),
    ("Dao", "DAO"),
    ("Entity", "ENTITY"),
    ("RepositoryImpl", "REPOSITORY_IMPL"),
    ("Repository", "REPOSITORY_INTERFACE"),
    ("UseCase", "USECASE"),
    ("Facade", "FACADE"),
    ("Service", "SERVICE"),
    ("Database", "DATABASE"),
    ("Nav", "NAVIGATION"),
]

KEYWORD_RULES = {
    "VIEWMODEL": ["ViewModel", "MutableStateFlow", "StateFlow"],
    "SCREEN": ["@Composable"],
    "DAO": ["@Dao"],
    "ENTITY": ["@Entity"],
    "DATABASE": ["RoomDatabase"],
}
