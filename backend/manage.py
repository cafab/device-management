import click
import random, string
import decimal
import datetime
import names
from flask.cli import FlaskGroup
from src.app import create_app
from src.models import db, User, Computer, PurchaseDetails, Accounts


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
        # Create computer object
        serial_number = "".join(random.choices(string.ascii_letters + string.digits, k=10)).upper()
        computer_name = "PC-" + str(i+1)
        ip_address = "192.168.0." + str(random.randrange(10, 255))
        timestamp = datetime.datetime.utcnow()
        os = "Windows 10 Pro, 1909, 64-bit"
        os_install_date = datetime.date(2017, 1, 1) + datetime.timedelta(days=random.randrange(1200))
        computer_model = "HP ProBook 650 G" + str(random.randrange(1, 5))
        cpu = "Intel(R) Core(TM) i5-4300M CPU @ 2.6GHz"
        memory = "8 GB"
        hard_disk = random.choice(["256 GB, SSD", "128 GB, SSD", "256 GB, HDD"])
            
        computer = Computer( 
            serial_number=serial_number,
            computer_name=computer_name, 
            ip_address=ip_address, 
            timestamp=timestamp,
            os=os,
            os_install_date=os_install_date,
            computer_model=computer_model,
            cpu=cpu,
            memory=memory,
            hard_disk=hard_disk
        )

        # Create purchase_details object
        supplier = random.choice(["Digitec", "STEG Electronics", "Microspot", "Brack"])
        price = float(decimal.Decimal(random.randrange(1000, 10000))/100) + float(random.randint(900,1400))
        purchase_date = datetime.date(2020, 1, 1) + datetime.timedelta(days=random.randrange(365))
        
        purchase_details = PurchaseDetails(
            supplier=supplier, 
            price=price, 
            purchase_date=purchase_date, 
            computer=computer
        )

        # Create accounts object
        current_account = names.get_first_name()[:1].lower() + names.get_last_name()[:2].lower()
        previous_account = names.get_first_name()[:1].lower() + names.get_last_name()[:2].lower()

        accounts = Accounts(
            current_account=current_account, 
            previous_account=previous_account,
            computer=computer
        )

        
        db.session.add(computer)
        db.session.add(purchase_details)
        db.session.add(accounts)
    
    db.session.commit()

    click.echo(str(number_of_devices) + " devices and purchase details have been created.\n")


@cli.command("seed_db")
def seed_db():
    create_db()
    create_admin()
    

@cli.command("create_devices")
def seed_devices():
    create_devices()


if __name__ == "__main__":
    cli()