import click
from flask.cli import FlaskGroup
from src.app import create_app
from src.models import db, User


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    pass


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("create_admin")
def create_admin():
    user = User(
        username="admin",
        password="$argon2id$v=19$m=102400,t=2,p=8$FPDTJjbccR4Azw3UDVR2tQ$Qi+ZjNQbJ/Ke+R8xwHBbug"
    )
    db.session.add(user)
    db.session.commit()
    click.echo("Login account created:")
    click.echo("Username: admin")
    click.echo("Password: admin")


if __name__ == "__main__":
    cli()