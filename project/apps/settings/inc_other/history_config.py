OBSERVED_FIELDS = {
    'accounts.User':
        (
            'username', 'first_name', 'middle_name', 'last_name', 'gender', 'phone', 'email',
            'photo', 'birthday',
        ),
    'accounts.BankCard':
        (
            'bank_name', 'bank_alias', 'card_number', 'card_holder', 'expiry_date',
        ),
    'accounts.IdentityDocument':
        (
            'document_type', 'series', 'number', 'birthplace', 'date_issue', 'date_expiration',
        ),
}
