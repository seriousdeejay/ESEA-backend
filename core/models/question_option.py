from django.db import models
from ..apps import AppConfig

# Change to Answer Option
class QuestionOption(models.Model):
    question = models.ForeignKey('Question', related_name="options", on_delete=models.CASCADE)
    question_responses = models.ManyToManyField('QuestionResponse', related_name='vals', blank=True) # Can this be removed safely?

    order = models.IntegerField(default=1)
    text = models.CharField(max_length=255, blank=False)
    value = models.IntegerField(blank=False) # Change to number?

    class Meta:
        db_table = 'f{AppConfig.name}_question_option'
    
    def equal(self, data):
        return self.text == data['text'] and self.value == data['value']
    
    def __str__(self):
        return f"{self.text}"

    def __repr__(self):
        return (f"text='{self.text} '")
        