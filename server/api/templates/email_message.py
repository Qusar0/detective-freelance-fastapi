from datetime import datetime
from server.api.conf.config import settings

def get_confirmation_email(email: str, confirm_url: str) -> dict:
    """Генерирует красивое письмо подтверждения"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background-color: #4a6fa5;
                padding: 20px;
                text-align: center;
                color: white;
                border-radius: 5px 5px 0 0;
            }}
            .content {{
                padding: 25px;
                background-color: #f9f9f9;
                border-radius: 0 0 5px 5px;
            }}
            .button {{
                display: inline-block;
                padding: 12px 24px;
                background-color: #4a6fa5;
                color: white !important;
                text-decoration: none;
                border-radius: 4px;
                font-weight: bold;
                margin: 15px 0;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 12px;
                color: #777;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h2>Подтверждение регистрации</h2>
        </div>
        
        <div class="content">
            <p>Добро пожаловать в наш сервис!</p>
            
            <p>Для завершения регистрации нажмите на кнопку ниже:</p>
            
            <p style="text-align: center;">
                <a href="{confirm_url}" class="button">Подтвердить Email</a>
            </p>
            
            <p>Или скопируйте и вставьте эту ссылку в браузер:</p>
            <p><code>{confirm_url}</code></p>
            
            <div class="footer">
                <p>Если вы не регистрировались, проигнорируйте это письмо.</p>
                <p>Информационно-аналитическая система «Детектив» | Служба поддержки: support@ias-detective.io</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_content = f"""
    Подтверждение регистрации
    
    Для завершения регистрации перейдите по ссылке:
    {confirm_url}
    
    Если вы не регистрировались, проигнорируйте это письмо.
    
    Информационно-аналитическая система «Детектив» | Служба поддержки: support@ias-detective.io
    """
    
    return {
        "subject": "Подтвердите ваш email",
        "recipients": [email],
        "html": html_content,
        "body": text_content
    }


def get_beware_email(email: str) -> ...:
    ...


def get_already_registered_email(email: str, login_url: str) -> dict:
    """Генерирует письмо для уже зарегистрированного пользователя"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background-color: #f39c12;
                padding: 20px;
                text-align: center;
                color: white;
                border-radius: 5px 5px 0 0;
            }}
            .content {{
                padding: 25px;
                background-color: #f9f9f9;
                border-radius: 0 0 5px 5px;
            }}
            .button {{
                display: inline-block;
                padding: 12px 24px;
                background-color: #f39c12;
                color: white !important;
                text-decoration: none;
                border-radius: 4px;
                font-weight: bold;
                margin: 15px 0;
            }}
            .alert {{
                background-color: #f8d7da;
                color: #721c24;
                padding: 10px;
                border-radius: 4px;
                margin: 15px 0;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 12px;
                color: #777;
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h2>Ваш аккаунт уже существует</h2>
        </div>
        
        <div class="content">
            <p>Здравствуйте!</p>
            
            <div class="alert">
                <p>Мы получили запрос на регистрацию для email <strong>{email}</strong>, 
                но этот адрес уже зарегистрирован в нашем сервисе.</p>
            </div>
            
            <p>Если это были вы, вы можете:</p>
            
            <p style="text-align: center;">
                <a href="{login_url}" class="button">Войти в аккаунт</a>
            </p>
            
            <p>Или скопируйте и вставьте эту ссылку в браузер:</p>
            <p><code>{login_url}</code></p>
            
            <p>Если вы не пытались зарегистрироваться, пожалуйста:</p>
            <ul>
                <li>Проигнорируйте это письмо</li>
                <li>Измените пароль, если у вас есть подозрения о несанкционированном доступе</li>
            </ul>
            
            <div class="footer">
                <p>Информационно-аналитическая система «Детектив» | Служба поддержки: support@ias-detective.io</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_content = f"""
    Ваш аккаунт уже существует
    
    Мы получили запрос на регистрацию для email {email}, 
    но этот адрес уже зарегистрирован в нашем сервисе.
    
    Если это были вы, перейдите по ссылке для входа:
    {login_url}
    
    Если вы не пытались зарегистрироваться:
    - Проигнорируйте это письмо
    - Измените пароль, если есть подозрения о несанкционированном доступе
    
    Информационно-аналитическая система «Детектив» | Служба поддержки: support@ias-detective.io
    """
    
    return {
        "subject": "Ваш аккаунт уже зарегистрирован",
        "recipients": [email],
        "html": html_content,
        "body": text_content
    }