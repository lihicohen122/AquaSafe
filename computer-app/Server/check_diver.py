from database import SessionLocal
from models.diver import Diver
from models.group import Group

def check_diver(diver_id="li"):
    db = SessionLocal()
    try:
        diver = db.query(Diver).filter(Diver.id == diver_id).first()
        if diver:
            print(f"Found diver {diver_id}:")
            print(f"  Name: {diver.name}")
            print(f"  BPM: {diver.bpm}")
            print(f"  Status: {diver.status}")
            print(f"  Group: {diver.group.name if diver.group else 'No Group'}")
        else:
            print(f"No diver found with ID {diver_id}")
    except Exception as e:
        print(f"Error checking diver: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_diver() 