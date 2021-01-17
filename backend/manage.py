import click
import random, string
import decimal
from datetime import date
from flask.cli import FlaskGroup
from src.app import create_app
from src.models import db, User, Computer, PurchaseDetails


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    pass


def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    click.echo("\nDatabase created.\n")


def create_admin():
    user = User(
        username="admin",
        password="$argon2id$v=19$m=102400,t=2,p=8$Ruxuuemw1/vzVi8TF9olyg$VzyjnND/p1Fc7Le+KF3lCQ"
    )
    db.session.add(user)
    db.session.commit()
    click.echo("Login account created:")
    click.echo("  Username: admin")
    click.echo("  Password: pass\n")


def create_devices():
    number_of_devices = 10
    
    # Create computers and purchase details
    computer_list = []
    for i in range(number_of_devices):
        serial_number = "".join(random.choices(string.ascii_letters + string.digits, k=10)).upper()
        computer_name = "PC-" + str(i+1)
        # Create computer object
        computer = Computer(serial_number=serial_number, computer_name=computer_name)
  
        supplier = random.choice(["Digitec", "STEG Electronics", "Microspot", "Brack"])
        price = float(decimal.Decimal(random.randrange(1000, 10000))/100) + float(random.randint(900,1400))
        purchase_date = date(year=2020, month=random.randint(1,12), day=random.randint(1,28))
        # Create purchase_details object
        purchase_details = PurchaseDetails(supplier=supplier, price=price, purchase_date=purchase_date, computer=computer)
        
        db.session.add(computer)
        db.session.add(purchase_details)
        db.session.commit()

    click.echo(str(number_of_devices) + " devices and purchase details have been created.\n")


@cli.command("seed_db")
def seed_db():
    create_db()
    create_admin()
    create_devices()

@cli.command("drop_db")
def drop_db():
    db.drop_all()
    click.echo("\nDatabase dropped.\n")


if __name__ == "__main__":
    cli()