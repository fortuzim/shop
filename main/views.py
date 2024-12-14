
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from app import settings
from django.core.mail import send_mail
from main.forms import ContactForm
from django.contrib import messages



def regulamin(request):
    return render(request, 'main/regulamin.html')

def onas(request):
    return render(request, 'main/onas.html')

def privacy(request):
    return render(request, 'main/privacy.html')

def contact(request):
    return render(request, 'main/contact.html')

class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Главная'
        context['content'] = "Магазин мебели HOME"
        return context


class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - О нас'
        context['content'] = "О нас"
        context['text_on_page'] = "Текст о том почему этот магазин такой классный, и какой хороший товар."
        context['form'] = ContactForm

        return context
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']

            try:
                send_mail(subject, message, email, ['karpienkovitaliy@gmail.com'])
                messages.success(request, 'Письмо отправлено')
                return redirect('main:index')  # Перенаправление на другую страницу
            except Exception as e:
                messages.error(request, f"Ошибка отправки: {e}")

        # Если форма не валидна или отправка не удалась, перерендерим страницу с формой
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)
    
# def index(request):

#     context = {
#         'title': 'Home - Главная',
#         'content': "Магазин мебели HOME",
#     }

#     return render(request, 'main/index.html', context)


# def about(request):
#     context = {
#         'title': 'Home - О нас',
#         'content': "О нас",
#         'text_on_page': "Текст о том почему этот магазин такой классный, и какой хороший товар."
#     }

#     return render(request, 'main/about.html', context)