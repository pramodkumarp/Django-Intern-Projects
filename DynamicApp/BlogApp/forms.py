from django import forms
import re
from BlogApp.models import *



class NameForm(forms.Form):
    fname = forms.CharField(
        label="Name",
        widget=forms.TextInput(attrs={'class':'fname', 'id':'fname', 'placeholder':'Enter user name'}),
        required=False,
        max_length=30,
    )
    lname = forms.CharField(
        label="Surname",
        widget=forms.TextInput(attrs={'class': 'lname', 'id': 'lname', 'placeholder': 'Enter surname'}),
        required=False,
        max_length=30,
    )
    def clean_fname(self):
        fname = self.cleaned_data['fname']
        if fname.__eq__(""):
            raise forms.ValidationError("Name field is required!")
        if not re.match("^[a-zA-Z\s]+$", fname):
            raise forms.ValidationError("Enter a valid name!")
        return fname.strip()

    def clean_lname(self):
        lname = self.cleaned_data['lname']
        if lname.__eq__(""):
            raise forms.ValidationError("Surname field is required!")
        if not re.match("^[a-zA-Z\s]+$", lname):
            raise forms.ValidationError("Enter a valid surname!")
        return lname.strip()


class GenderForm(forms.Form):
    genders = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = forms.ChoiceField(
        label="Gender",
        widget=forms.RadioSelect(attrs={'class':'gender', 'id':'gender'}),
        choices=genders,
        required=False,
    )

    def clean_gender(self):
        gender = self.cleaned_data['gender']
        if gender.__eq__(""):
            raise forms.ValidationError("Gender selection is required!")
        return gender


class BirthDayForm(forms.Form):
    days = (
        ('', '- dd -'),('01', '01'),('02', '02'),('03', '03'),('04', '04'),('05', '05'),('06', '06'),('07', '07'),('08', '08'),('09', '09'),('10', '10'),('11', '11'),('12', '12'),('13', '13'),('14', '14'),('15', '15'),('16', '16'),('17', '17'),('18', '18'),('19', '19'),('20', '20'),('21', '21'),('22', '22'),('23', '23'),('24', '24'),('25', '25'),('26', '26'),('27', '27'),('28', '28'),('29', '29'),('30', '30'),('31', '31')
    )
    birthday = forms.ChoiceField(
        label="Date of Birth",
        widget=forms.Select(attrs={'class':'birthday', 'id':'birthday'}),
        choices=days,
        required=False,
    )
    def clean_birthday(self):
        birthday = self.cleaned_data['birthday']
        if birthday.__eq__(""):
            raise forms.ValidationError("Birth day selection required!")
        return birthday

    months = (
        ('', '-- mm --'), ('01', '01-Jan'), ('02', '02-Feb'), ('03', '03-Mar'), ('04', '04-Apr'), ('05', '05-May'), ('06', '06-Jun'), ('07', '07-Jul'), ('08', '08-Aug'), ('09', '09-Sep'), ('10', '10-Otc'), ('11', '11-Nov'), ('12', '12-Dec')
    )
    birthmonth = forms.ChoiceField(
        label="Date of Birth",
        widget=forms.Select(attrs={'class': 'birthmonth', 'id': 'birthmonth'}),
        choices=months,
        required=False,
    )
    def clean_birthmonth(self):
        birthmonth = self.cleaned_data['birthmonth']
        if birthmonth.__eq__(""):
            raise forms.ValidationError("Birth month selection required!")
        return birthmonth

    years = (
        ('', '-- yyyy --'), ('2019', '2019'), ('2018', '2018'), ('2017', '2017'), ('2016', '2016'), ('2015', '2015'), ('2014', '2014'),  ('2013', '2013'), ('2012', '2012'),('2011', '2011'), ('2010', '2010'),('2009', '2009'), ('2008', '2008'),('2007', '2007'),('2006', '2006'),('2005', '2005'),('2004', '2004'),('2003', '2003'),('2002', '2002'),  ('2001', '2001'),('2000', '2000'),('1999', '1999'),('1998', '1998'),('1997', '1997'),('1996', '1996'),('1995', '1995'),('1994', '1994'),('1993', '1993'),('1992', '1992'),('1991', '1991'),('1990', '1990'),('1989', '1989'), ('1988', '1988'),('1987', '1987'),('1986', '1986'),('1985', '1985'),('1984', '1984'),('1983', '1983'), ('1982', '1982'), ('1981', '1981'),('1980', '1980'), ('1979', '1979'), ('1978', '1978'), ('1977', '1977'), ('1976', '1976'), ('1975', '1975'), ('1974', '1974'), ('1973', '1973'), ('1972', '1972'), ('1971', '1971'),('1970', '1970'),
    )
    birthyear = forms.ChoiceField(
        label="Date of Birth",
        widget=forms.Select(attrs={'class': 'birthyear', 'id': 'birthyear'}),
        choices=years,
        required=False,
    )
    def clean_birthyear(self):
        birthyear = self.cleaned_data['birthyear']
        if birthyear.__eq__(""):
            raise forms.ValidationError("Birth year selection required!")
        return birthyear


class UserForm(forms.Form):
    email = forms.EmailField(
        label="E-mail Address",
        widget=forms.TextInput(attrs={'class':'email', 'id':'email', 'placeholder':'Enter email address'}),
        required=False,
        max_length=50,
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if email.__eq__(""):
            raise forms.ValidationError("E-mail field is required!")
        if not re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            raise forms.ValidationError("Email format isn't valid!")
        if UserTable.objects.filter(email_address=email, email_validity=1).exists():
            raise forms.ValidationError("Email already in use!")
        else:
            user = UserTable.objects.filter(email_address=email)
            user.delete()
        return email.strip()

    password =forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class':'password', 'id':'password', 'placeholder':'Enter a password'}),
        required=False,
        max_length=30,
    )

    confirm_password=forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class':'confirm_password', 'id':'confirm_password', 'placeholder':'Confirm your password'}),
        required=False,
        max_length=30,
    )
    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if confirm_password.__eq__("") and password.__eq__(""):
            raise forms.ValidationError("Password field is required!")
        if len(confirm_password).__le__(4):
            raise forms.ValidationError("Password length minimum 4 charters allowed!")
        if len(confirm_password).__ge__(31):
            raise forms.ValidationError("Password length maximum 30 charters allowed!")
        if password.__ne__(confirm_password):
            raise forms.ValidationError("Password matching error!")
        return confirm_password


class EmailConfirmCode(forms.Form):
    code = forms.CharField(
        label="Email Verification Code",
        widget=forms.TextInput(attrs={'class':'code','id':'code', 'placeholder':'Enter verification code'}),
        required=False,
    )
    def clean_code(self):
        code = self.cleaned_data['code']
        if code.__eq__(""):
            raise forms.ValidationError("Verification code is required!")
        if not re.match("^[0-9]*$", code):
            raise forms.ValidationError("Only numeric is allowed!")
        return code.strip()


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='E-mail Address',
        widget=forms.TextInput(attrs={'class':'email', 'id':'email', 'placeholder':'Enter email address'}),
        required=False,
        max_length=30,
    )
    def clean_email(self):
        email = self.cleaned_data['email']
        if email.__eq__(""):
            raise forms.ValidationError("E-mail field is required!")
        if not re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            raise forms.ValidationError("Email format isn't valid!")
        return email.strip()

    password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={'class': 'confirm_password', 'id': 'confirm_password', 'placeholder': 'Confirm your password'}),
        required=False,
        max_length=30,
    )
    def clean_password(self):
        password = self.cleaned_data['password']
        if password.__eq__("") and password.__eq__(""):
            raise forms.ValidationError("Password field is required!")
        if len(password).__le__(4):
            raise forms.ValidationError("Password length minimum 4 charters allowed!")
        if len(password).__ge__(31):
            raise forms.ValidationError("Password length maximum 30 charters allowed!")
        if password.__ne__(password):
            raise forms.ValidationError("Password matching error!")
        return password


class AddressForm(forms.Form):
    village = forms.CharField(
        label="Village Name",
        widget=forms.TextInput(attrs={'class':'vlg_name', 'id':'vlg_name', 'placeholder':'Enter village name'}),
        required=False,
    )
    def clean_village(self):
        vlg = self.cleaned_data['village']
        if vlg.__eq__(""):
            raise forms.ValidationError("Village address is required!")
        if len(vlg).__ge__(100):
            raise forms.ValidationError("Length is <100 required!")
        if not re.match("^[a-zA-Z\s]+$", vlg):
            raise forms.ValidationError("Village name is not valid!")
        return vlg

    city = forms.CharField(
        label="City Name",
        widget=forms.TextInput(attrs={'class': 'cty_name', 'id': 'cty_name', 'placeholder': 'Enter city name'}),
        required=False,
    )
    def clean_city(self):
        city = self.cleaned_data['city']
        if city.__eq__(""):
            raise forms.ValidationError("City address is required!")
        if len(city).__ge__(100):
            raise forms.ValidationError("Length is <100 required!")
        if not re.match("^[a-zA-Z\s]+$", city):
            raise forms.ValidationError("City name is not valid!")
        return city

    zip = forms.CharField(
        label="Zip Code",
        widget=forms.TextInput(attrs={'class': 'zip_code', 'id': 'zip_code', 'placeholder': 'Enter zip code'}),
        required=False,
    )
    def clean_zip(self):
        zip = self.cleaned_data['zip']
        if zip.__eq__(""):
            raise forms.ValidationError("Zip code is required!")
        if len(zip).__ge__(100):
            raise forms.ValidationError("Length is <20 required!")
        return zip

    countries = (
        ('','-- Select Country --'),
        ('Bangladesh', 'Bangladesh'),
        ('India', 'India'),
        ('Pakistan', 'Pakistan'),
        ('Australia', 'Australia'),
        ('Botswana', 'Botswana'),
    )
    country = forms.ChoiceField(
        label="Your Country",
        widget=forms.Select(attrs={'class': 'country_name', 'id': 'country_name'}),
        required=False,
        choices=countries,
    )
    def clean_country(self):
        country = self.cleaned_data['country']
        if country.__eq__(""):
            raise forms.ValidationError("Country selection is required!")
        return country



class UploadImage(forms.Form):
    upimage = forms.ImageField(
        label="Upload Profile Image",
        widget=forms.FileInput(attrs={'class':'image', 'id':'image'}),
        required=False,
    )
    def clean_upimage(self):
        image = self.cleaned_data['upimage']
        if image is None:
            raise forms.ValidationError("Image selection required!")
        if image.content_type.__ne__('image/jpeg'):
            raise forms.ValidationError("Only JPEG format is acceptable!")
        if image.size.__gt__(1024*1024):
            raise forms.ValidationError("File size 1MB required!")
        return image


class PostForm(forms.Form):
    title = forms.CharField(
        label="Enter post title",
        widget=forms.TextInput(attrs={'class':'title', 'id':'title', 'placeholder':'Enter post title'}),
        max_length=200,
        min_length=10,
        required=False,
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'description', 'id': 'description', 'placeholder': 'Enter post description ........', 'cols':81, 'rows':5}),
        max_length=200,
        min_length=10,
        required=False,
    )
    postimage = forms.ImageField(
        label="Upload a post related image",
        widget=forms.FileInput(attrs={'class': 'postimage', 'id': 'postimage'}),
        required=False,
    )