from app.database import SessionLocal, Base, engine
from app.models import Organization, User
from app.auth import get_password_hash

Base.metadata.create_all(bind=engine)
db = SessionLocal()

police_org = db.query(Organization).filter(Organization.name == "Delhi AHTU Unit").first()
if not police_org:
    police_org = Organization(
        name="Delhi AHTU Unit",
        org_type="POLICE",
        state="Delhi",
        district="Central Delhi"
    )
    db.add(police_org)

ngo_org = db.query(Organization).filter(Organization.name == "Bachpan Suraksha NGO").first()
if not ngo_org:
    ngo_org = Organization(
        name="Bachpan Suraksha NGO",
        org_type="NGO",
        state="Delhi",
        district="South Delhi"
    )
    db.add(ngo_org)

db.commit()
db.refresh(police_org)
db.refresh(ngo_org)

if not db.query(User).filter(User.email == "police@gumshuda.org").first():
    police_user = User(
        email="police@gumshuda.org",
        hashed_password=get_password_hash("policePass123"),
        full_name="Inspector R. Sharma",
        role="POLICE_OFFICER",
        badge_or_id="DL-AHTU-402",
        organization_id=police_org.id
    )
    db.add(police_user)

if not db.query(User).filter(User.email == "ngo@gumshuda.org").first():
    ngo_user = User(
        email="ngo@gumshuda.org",
        hashed_password=get_password_hash("ngoPass123"),
        full_name="Pooja Verma",
        role="NGO_STAFF",
        organization_id=ngo_org.id
    )
    db.add(ngo_user)

if not db.query(User).filter(User.email == "admin@gumshuda.org").first():
    admin_user = User(
        email="admin@gumshuda.org",
        hashed_password=get_password_hash("adminPass123"),
        full_name="System Administrator",
        role="ADMIN",
        organization_id=police_org.id
    )
    db.add(admin_user)

db.commit()
print("Seeding complete: Verified police, NGO, and Admin accounts initialized.")
db.close()