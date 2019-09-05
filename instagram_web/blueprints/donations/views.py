import re
import braintree
import os
from flask import Blueprint, render_template, url_for, request, redirect, flash, abort
from models.user import User
from models.image import Image
from models.donations import Donation
from flask_login import logout_user, login_required, current_user
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

donations_blueprint = Blueprint('donations',
                            __name__,
                            template_folder='templates')

gateway = braintree.BraintreeGateway(
    braintree.Configuration(
        braintree.Environment.Sandbox,
        merchant_id= os.environ.get("merchant_id"),
        public_key= os.environ.get("public_key"),
        private_key= os.environ.get("private_key"),
    )
)

@donations_blueprint.route('/donate/<username>/<id>', methods=["GET"])
@login_required
def new(id, username):
    client_token = gateway.client_token.generate()
    return render_template('/donations/new.html',client_token=client_token, id=id)

@donations_blueprint.route('/checkout/<id>', methods=["POST"])
@login_required
def create_donation(id):
    nonce_from_the_client = request.form["this-input"]
    amount = request.form.get('this-amount')
    gateway.transaction.sale({
        "amount":amount,
        "payment_method_nonce": nonce_from_the_client,
        "options": {
            "submit_for_settlement":True
        }
    })
    Donation(amount=amount, image=id , user=current_user.username).save()
    
    image = Image.get_by_id(id)
    user = User.get_or_none(User.id == image.user_id)
    message = Mail(
        from_email = 'nextagram@example.com',
        to_emails = user.email,
        subject='Donation Notification',
        html_content= '@' + current_user.username + ' donated' + f' ${amount} to the following image below!<br><img src="{ image.upload_image_url }" />')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))
    return redirect(url_for('home'))