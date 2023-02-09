from django import forms

class registrationform(forms.Form):
    firstname=forms.CharField(max_length=25)
    lastname=forms.CharField(max_length=25)
    username = forms.CharField(max_length=25)
    email = forms.EmailField()
    password = forms.CharField(max_length=20)
    cpassword=forms.CharField(max_length=20)


class loginform(forms.Form):
    username=forms.CharField(max_length=25)
    password=forms.CharField(max_length=20)

class uploadform(forms.Form):
    name = forms.CharField(max_length=20)
    price = forms.IntegerField()
    description = forms.CharField(max_length=50)
    image = forms.ImageField()

class Contactusform(forms.Form):
    Name=forms.CharField(max_length=30)
    Email=forms.EmailField()
    Message=forms.CharField(max_length=500)