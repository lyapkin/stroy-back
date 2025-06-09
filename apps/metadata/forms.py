from django import forms


class MetadataInlineFormModel(forms.ModelForm):
    title = forms.CharField(label="title", max_length=255, required=False)
    description = forms.CharField(label="description", widget=forms.Textarea, required=False)

    def has_changed(self):
        title = self.initial.get("title", None)
        description = self.initial.get("description", None)
        if not title or not description or len(title) == 0 or len(description) == 0:
            return True
        return super().has_changed()

    def save(self, commit=...):
        if len(self.cleaned_data["title"]) == 0:
            self.instance.generate_title()
        if len(self.cleaned_data["description"]) == 0:
            self.instance.generate_description()
        return super().save(commit)
