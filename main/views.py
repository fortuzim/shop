from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.core.mail import send_mail
from main.forms import ContactForm
from django.contrib import messages


class StaticPageView(TemplateView):
    allowed_pages = ["regulamin", "onas", "privacy", "contact"]

    def get_template_names(self) -> list[str]:
        page_name = self.kwargs.get("page_name")
        if page_name in self.allowed_pages:
            return [f"main/{page_name}.html"]
        raise Http404("Page not found")


class IndexView(TemplateView):
    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Главная"
        context["content"] = "Магазин мебели HOME"
        return context


class AboutView(TemplateView):
    template_name = "main/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - О нас"
        context["content"] = "О нас"
        context["text_on_page"] = (
            "Текст о том почему этот магазин такой классный, и какой хороший товар."
        )
        context["form"] = ContactForm

        return context

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            email = form.cleaned_data["email"]

            try:
                send_mail(subject, message, email, ["karpienkovitaliy@gmail.com"])
                messages.success(request, "Письмо отправлено")
                return redirect("main:index")  # Перенаправление на другую страницу
            except Exception as e:
                messages.error(request, f"Ошибка отправки: {e}")

        # Если форма не валидна или отправка не удалась, перерендерим страницу с формой
        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)
