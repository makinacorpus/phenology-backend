from modeltranslation.translator import translator, TranslationOptions
from backend import models


# Species
class SpeciesTO(TranslationOptions):
    fields = ('name', 'description', )


# Species
class StageTO(TranslationOptions):
    fields = ('name', )

# Register previously defined translation options
backend_translation_to_register = [
    (models.Species, SpeciesTO),
    (models.Stage, StageTO),
]

for model, model_to in backend_translation_to_register:
    translator.register(model, model_to)
