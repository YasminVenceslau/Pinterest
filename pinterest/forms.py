from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Pin, Profile
from django.forms.widgets import ClearableFileInput

# --- Widget customizado para upload de imagem sem preview e sem texto "Currently/Change" ---
class CustomClearableFileInput(ClearableFileInput):
    template_name = 'widgets/custom_clearable_file_input.html'

# --- Formulário para atualizar perfil ---
class ProfilePicForm(forms.ModelForm):
    profile_image = forms.ImageField(
        label="Foto de Perfil",
        required=False,
        widget=CustomClearableFileInput(attrs={
            'class': 'form-control pinterest-input',
            'style': (
                'border-radius: 12px; padding: 12px; '
                'background-color: #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'
            )
        })
    )

    class Meta:
        model = Profile
        fields = ['profile_image']

# --- Formulário de cadastro de usuário ---
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control pinterest-input',
            'placeholder': 'Nome',
            'style': (
                'border-radius: 12px; padding: 12px; '
                'background-color: #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'
            )
        })
    )
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(attrs={
            'class': 'form-control pinterest-input',
            'placeholder': 'Endereço de e-mail',
            'style': (
                'border-radius: 12px; padding: 12px; '
                'background-color: #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'
            )
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Estilizando o campo username
        self.fields['username'].widget.attrs.update({
            'class': 'form-control pinterest-input',
            'placeholder': 'Seu nome de usuário',
            'style': (
                'border-radius: 12px; padding: 12px; '
                'background-color: #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'
            )
        })
        self.fields['username'].label = ''
        self.fields['username'].help_text = (
            '<span class="form-text text-muted small">'
            'Máx. 150 caracteres. Letras, números e @/./+/-/_.</span>'
        )

        # Estilizando password1 e password2
        for field_name, placeholder, help_text in [
            ('password1', 'Senha',
             '<ul class="form-text text-muted small">'
             '<li>Deve ter 8+ caracteres.</li>'
             '<li>Inclua letras, números e símbolo.</li></ul>'),
            ('password2', 'Confirme sua senha',
             '<span class="form-text text-muted small">Digite a mesma senha novamente.</span>')
        ]:
            field = self.fields[field_name]
            field.widget.attrs.update({
                'class': 'form-control pinterest-input',
                'placeholder': placeholder,
                'style': (
                    'border-radius: 12px; padding: 12px; '
                    'background-color: #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'
                )
            })
            field.label = ''
            field.help_text = help_text

# --- Formulário para criar/editar Pin ---
class PinForm(forms.ModelForm):
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "placeholder": "Descreva seu Pin...",
            "class": "form-control pinterest-textarea",
            "rows": 3,
            "style": (
                "border-radius: 12px; padding: 12px; resize: none; "
                "background-color: #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.1);"
            )
        }),
        label=""
    )
    image = forms.ImageField(
        label="",
        widget=CustomClearableFileInput(attrs={
            'class': 'form-control pinterest-input',
            'style': (
                'border-radius: 12px; padding: 12px; '
                'background-color: #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'
            )
        })
    )

    class Meta:
        model = Pin
        fields = ("image", "description")
