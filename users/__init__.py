def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['password1'].label = 'Пароль'
    self.fields['password2'].label = 'Подтверждение пароля'