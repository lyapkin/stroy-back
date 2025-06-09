from django.contrib import admin, messages


class MetaGenerationRuleMixin:

    def generate_title(self):
        rule = self.rule
        self.title = rule.title.format(name=self.entity.name)

    def generate_description(self):
        rule = self.rule
        self.description = rule.description.format(name=self.entity.name)


class MetaGenrationActionMixin:

    @admin.action(description="Сгенерировать метаданные")
    def generate_metadata(self, request, qs):
        SEOModel = self.model.metadata.related.related_model
        update_list = []
        qs = qs.select_related("metadata__rule")
        for entity in qs:
            metadata = entity.metadata

            metadata.generate_title()
            metadata.generate_description()

            update_list.append(metadata)

        SEOModel.objects.bulk_update(update_list, ["title", "description"], 1000)

        self.message_user(
            request,
            f"Метаданные сгенерированны",
            messages.SUCCESS,
        )
