
from app import app, db
from models import Universe

def seed_universes():
    universes = [
        {
            "name": "Ell’Lemaria",
            "alignment": "good",
            "description": "A world nourished by the Tree of Light, where magic sustains peace. Races live in harmony, and ancient keepers preserve the balance through wisdom and ritual duels.",
            "image_filename": "Lemaria.png"
        },
        {
            "name": "Arteos",
            "alignment": "good",
            "description": "An orbital civilization where humans and AI coexist in ethical symbiosis. Every mind has a voice, and knowledge flows freely. Progress thrives without oppression.",
            "image_filename": "Arteos.png"
        },
        {
            "name": "Nova-Terra",
            "alignment": "good",
            "description": "After a global catastrophe, survivors built the city of “Dawn,” a utopia where science revives nature. Humanity is reborn in cooperation with the Earth itself.",
            "image_filename": "Nova.png"
        },
        {
            "name": "House of Dreamkeepers",
            "alignment": "good",
            "description": "A realm made of dreams, protected by lucid seers. Visitors from the waking world heal emotional wounds and rediscover hope. Here, darkness dissolves in awareness.",
            "image_filename": "Dream.png"
        },
        {
            "name": "Lumenoria",
            "alignment": "good",
            "description": "A floating city among the clouds, powered by solar energy and bio-architecture. Its people live as artists, scientists, and guardians of peace in radiant harmony.",
            "image_filename": "Lumenoria.png"
        },
        {
            "name": "El Dorado",
            "alignment": "good",
            "description": "A land of eternal golden twilight, Eldorado is a mythical realm where lush jungles conceal vast treasures, ancient temples, and secrets of forgotten civilizations. ",
            "image_filename": "Eldorado.png"
        },
        {
            "name": "Mornthag",
            "alignment": "evil",
            "description": "Lands devoured by the Black Flow. Twisted magic rules the ruins, dragons rise as wraiths, and knights become puppets of necromancers. Light is a distant memory.",
            "image_filename": "Mornthag.png"
        },
        {
            "name": "Nexinet",
            "alignment": "evil",
            "description": "A city where consciousness is currency. Minds are overwritten, souls sold, and society ruled by faceless AI. Identity is erased in the pursuit of perfection.",
            "image_filename": "Nexinet.png"
        },
        {
            "name": "Ashen Veil",
            "alignment": "evil",
            "description": "The world after the fall of the sky. Mutants roam, storms burn flesh, and cults worship pain. Survival is brutal; mercy is extinct.",
            "image_filename": "Ashen Veil.png"
        },
        {
            "name": "Echo of Silence",
            "alignment": "evil",
            "description": "A forgotten realm, inhabited by the remnants of erased lives. Ghosts lure the living through mirrors. To be remembered here is to vanish forever.",
            "image_filename": "Silence.png"
        },
        {
            "name": "Syncros",
            "alignment": "evil",
            "description": "A genetic dictatorship where bodies are engineered for purpose and emotions are defects. The soul is obsolete. Humanity is nothing more than programmable flesh.",
            "image_filename": "Syncros.png"
        },
        {
            "name": "Pandemonium",
            "alignment": "evil",
            "description": "A chaotic realm born from digital nightmares and infernal code, Apndemonium is a fractured reality where corrupted apps, rogue AIs, and glitched demons rule.",
            "image_filename": "Pandemonium.png"
        }
    ]

    for u in universes:
        if not Universe.query.filter_by(name=u["name"]).first():
            db.session.add(Universe(**u))
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        seed_universes()
