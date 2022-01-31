from django import forms
from recipes.models import Recipe, RecipeIngredients

class RecipeForm(forms.ModelForm):
    required_css_class = 'required-field' # css classes have '-' between then not '_'
    error_css_class = 'error-field'
    
    # choose the 'name' as variable cause u are handling input area called 'name'
    ''
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Recipe Name'}), help_text='This is your help! <a href="../../../../">Contact us</a>')
    ''
    # you will forget the line above, make sure to check django documentations 
    # choose 'description' for the same reason. 
    # choose the name you want
    ''
    # description = forms.CharField(widget=forms.Textarea({'rows':'3'}))
    ''
    # interestingly, if you make a variable with a name outside your form elements
    # a new form will be created with the properties you gave it

    # yet another method to change those things:
    # we can use both, but the lines below will overwrite others
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_data = {
            'placeholder':f'Recipe {str(field)}',
            'class':'form-control',
            # 'hx-post':'.',
            # 'hx-trigger':'keyup changed delay:500ms',
            # 'hx-target':'#recipe-container',
            # 'hx-swap':'outerHTML'
        }
            self.fields[str(field)].widget.attrs.update(new_data) # you can pass **new_data too, in order to unpack it
        self.fields['name'].label= 'Naaaaaame!!!!'
        self.fields['name'].widget.attrs.update({'class':'form-control-2'})
        self.fields['description'].widget.attrs.update({'rows':'2'})
        self.fields['directions'].widget.attrs.update({'rows':'4'})



    class Meta:
        model = Recipe
        fields = ['name', 'description', 'directions']

    
class RecipeIngredientsForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredients
        fields = ['name', 'quantity', 'unit']
