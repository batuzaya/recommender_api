from api import app, db
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand

migrate = Migrate(app, db)
migration_manager = Manager(usage="Manage the database")
migration_manager.add_command('migrate', MigrateCommand)

@migration_manager.command
def create():
    """ Create the database """
    db.create_all()

@migration_manager.command
def drop():
    """ Empty the database """
    if prompt_bool("Are you sure you want to drop all tables from the database?"):
        db.drop_all()


@migration_manager.command
def recreate():
    """ Recreate the database """
    drop()
    create()

manager = Manager(app)
manager.add_command("database", migration_manager)

if __name__ == '__main__':
    manager.run()