from rest_framework import serializers

from ..models import TextFragment

class TextFragmentSerializer(serializers.ModelSerializer):
    section = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TextFragment
        fields = [
            'id', 
            'section', 
            'order', 
            'text'
        ]







        # def to_representation(self, instance):
        #     representation = super().to_representation(instance)
        #     representation['section'] = instance.section.title

        #     return representation