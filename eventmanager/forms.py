from django import forms


from django import forms


class FilterForm(forms.Form):
    filter = forms.CharField(label='Text Filter', required=True, max_length=20,
                             widget=forms.TextInput(attrs={
                                   "class": "form-control",
                                   "placeholder": "Text Filter"
                             })
                             )
    orderby = forms.CharField(label='Order By', required=True, max_length=20,
                             widget=forms.TextInput(attrs={
                                   "class": "form-control",
                                   "placeholder": "Order By"
                             })
                             )
    page = forms.CharField(label='Page Nr', required=True, max_length=20,
                             widget=forms.TextInput(attrs={
                                   "class": "form-control",
                                   "placeholder": "Page Nr"
                             })
                             )
    pagedby = forms.CharField(label='Rec Per Page', required=True, max_length=20,
                             widget=forms.TextInput(attrs={
                                   "class": "form-control",
                                   "placeholder": "Rec Per Page"
                             })
                             )

class LoginForm(forms.Form):

    username = forms.CharField(label='User Name', required=True, max_length=20,
                               widget=forms.TextInput(attrs={
                                   "class": "form-control",
                                   "placeholder": "User Name"
                               })
                               )
    password = forms.CharField(label='User Password',
                               required=True, max_length=20,
                               widget=forms.PasswordInput(attrs={
                                   "class": "form-control",
                                   "placeholder": "User Password"
                               },
                                   render_value=True)
                               )
    # add rememberme

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if not username or not password:
            raise forms.ValidationError('User Name or Password is Empty')
