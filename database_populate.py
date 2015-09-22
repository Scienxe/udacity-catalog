from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Category, Instrument

engine = create_engine('sqlite:///musicalinstruments.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create users
Users = []
Users.append(User(name = "Pete Fountain", 
             email = "pete@example.com",
             picture = "http://www.epluri.com/NOTfolder/NOTImages/PeteFountain.jpeg"))
Users.append(User(name = "Louis Armstrong", 
             email = "louis@example.com",
             picture = "http://ia.media-imdb.com/images/M/MV5BMTQ0NDUwMDQ1OF5BMl5BanBnXkFtZTYwNzM4MTM2._V1_SX640_SY720_.jpg"))
Users.append(User(name = "Yo Yo Ma", 
             email = "yoyo@example.com",
             picture = "https://pbs.twimg.com/profile_images/501212965664616448/M3LWWSHt.jpeg"))
Users.append(User(name = "Vladimir Horowitz",
             email = "vlad@example.com",
             picture = "http://keimform.de/wp-content/uploads/2012/01/Abbildung1.jpg"))
Users.append(User(name = "Neil Peart",
             email = "neil@example.com",
             picture = "https://i239.photobucket.com/albums/ff227/00joe00m00amma/neil-peart.jpg"))
for user in Users:
    session.add(user)

session.commit()


# Create categories
Categories = []
Categories.append(Category(name = "Woodwind",
                           description = "Woodwinds direct airflow across a reed, which then vibrates to produce sound.",
                           user_id = 1))
Categories.append(Category(name = "Brass",
                           description = "Brass instruments are played by vibrating the lips on a mouthpiece, causing the air in the instrument to vibrate in resonance.",
                           user_id = 2))
Categories.append(Category(name = "String",
                           description = "Stringed instruments produce sound by the vibration of a set of plucked or bowed strings.",
                           user_id = 3))
Categories.append(Category(name = "Keyboard",
                           description = "Keyboard instruments select the desired tone by pressing or striking one of a set of keys, planks, or buttons.",
                           user_id = 4))
Categories.append(Category(name = "Percussion",
                           description = "Percussion instruments are played by striking them with the hands, sticks, mallets, or other implement.",
                           user_id = 5))
for cat in Categories:
    session.add(cat)
session.commit()


# Create Woodwinds
Inst = []
Inst.append(Instrument(name = "Clarinet",
                       description = "A straight, reeded instrument, traditionally made of wood.",
                       picture = "http://media.musicarts.com/is/image/MMGS7/Bundy-BCL-300-Clarinet-Standard/463680000390000-00-250x250.jpg",
                       price = 99,
                       category_id = 1,
                       user_id = 1))
Inst.append(Instrument(name = "Oboe",
                       description = "A double reeded instrument, traditionally made of wood.",
                       picture = "http://www.dsokids.com/media/2289/photo160oboe.jpg",
                       price = 149,
                       category_id = 1,
                       user_id = 1))
Inst.append(Instrument(name = "Bassoon",
                       description = "A large, reeded instrument, traditionally made of wood.",
                       picture = "http://www.musicwithease.com/bassoon-3.jpg",
                       price = 199,
                       category_id = 1,
                       user_id = 1))
Inst.append(Instrument(name = "Alto Saxophone",
                       description = "A curved, reeded instrument, traditionally made of brass.",
                       picture = "http://media.musicarts.com/is/image/MMGS7/P--Mauriat-PMSA-57GC-Intermediate-Alto-Saxophone-Honey-Gold-Lacquer/H94365000001000-00-250x250.jpg",
                       price = 129,
                       category_id = 1,
                       user_id = 1))
Inst.append(Instrument(name = "Tenor Saxophone",
                       description = "A curved, reeded instrument, traditionally made of brass.",
                       picture = "http://media.wwbw.com/is/image/MMGS7/P--Mauriat-Le-Bravo-200-Intermediate-Tenor-Saxophone-Matte-finish/H72353000001000-00-250x250.jpg",
                       price = 169,
                       category_id = 1,
                       user_id = 1))

# Create Brasses
Inst.append(Instrument(name = "Trumpet",
                       description = "A brass instrument with three valves.",
                       picture = "http://realbraveaudio.com/wp-content/uploads/2013/03/trumpet-lessons.jpg",
                       price = 99,
                       category_id = 2,
                       user_id = 2))
Inst.append(Instrument(name = "Cornet",
                       description = "A brass instrument with three valves.",
                       picture = "https://images.static-thomann.de/pics/prod/188510.jpg",
                       price = 109,
                       category_id = 2,
                       user_id = 2))
Inst.append(Instrument(name = "Trombone",
                       description = "A brass instrument with a sliding segment.",
                       picture = "http://www.papakuramusicschool.org.nz/images/Trombone.jpg",
                       price = 199,
                       category_id = 2,
                       user_id = 2))
Inst.append(Instrument(name = "French Horn",
                       description = "A coiled brass instrument with three valves.",
                       picture = "http://www.lovemorerentals.co.za/userimages/French%20Horn%20Yam.jpg",
                       price = 219,
                       category_id = 2,
                       user_id = 2))
Inst.append(Instrument(name = "Tuba",
                       description = "A large brass instrument with three valves.",
                       picture = "http://www.amatiinstruments.com/tuba/img/abb_223gross.jpg",
                       price = 399,
                       category_id = 2,
                       user_id = 2))

# Create Strings
Inst.append(Instrument(name = "Guitar",
                       description = "A standard stringed instrument with six strings.",
                       picture = "http://static.stereogum.com/blogs.dir/2/files/2012/06/paul-simon-guitar.jpg",
                       price = 199,
                       category_id = 3,
                       user_id = 3))
Inst.append(Instrument(name = "Violin",
                       description = "A small, bowed string instrument with four strings.",
                       picture = "http://www.stewartfamilychiro.com/attachments/Image/violin_pictures__5.jpg",
                       price = 199,
                       category_id = 3,
                       user_id = 3))
Inst.append(Instrument(name = "Viola",
                       description = "A bowed string instrument with four strings.",
                       picture = "http://www.accademiapianistica.org/userfiles/images/DV016_Jpg_Large_470067_080_14-inch.jpg",
                       price = 209,
                       category_id = 3,
                       user_id = 3))
Inst.append(Instrument(name = "Cello",
                       description = "A large, bowed string instrument with four strings.",
                       picture = "https://static.musiciansfriend.com/derivates/6/001/240/982/DV019_Jpg_Regular_464364_with_cello.jpg",
                       price = 499,
                       category_id = 3,
                       user_id = 3))
Inst.append(Instrument(name = "Double Bass",
                       description = "A very large, bowed string instrument with four strings.",
                       picture = "http://www.caswells-strings.co.uk/shop/29-4523-thickbox/stentor-student.jpg",
                       price = 799,
                       category_id = 3,
                       user_id = 3))

# Create Keys
Inst.append(Instrument(name = "Piano",
                       description = "A hammered string instrument with 88 keys.",
                       picture = "http://hyperphysics.phy-astr.gsu.edu/hbase/music/imgmus/piano.jpg",
                       price = 1999,
                       category_id = 4,
                       user_id = 4))
Inst.append(Instrument(name = "Electric Piano",
                       description = "An 88-key instrument which mimics the sound of a piano.",
                       picture = "http://www.sonicscoop.com/site/wp-content/uploads/2012/09/USA_Krome_2.png",
                       price = 499,
                       category_id = 4,
                       user_id = 4))
Inst.append(Instrument(name = "Pipe Organ",
                       description = "A very large, installed instrument with resonating pipes.",
                       picture = "https://s3.amazonaws.com/images.fineartamerica.com/images-medium-large/skinner-pipe-organ-clarence-holmes.jpg",
                       price = 199999,
                       category_id = 4,
                       user_id = 4))

# Create Percussion
Inst.append(Instrument(name = "Snare Drum",
                       description = "A staccato sounding drum with a rattle of metal wires in contact with the bottom head.",
                       picture = "https://www.thomann.de/thumb/thumb300x/pics/cms/image/guide/en/snare_drums/0103_snare_unten.jpg",
                       price = 99,
                       category_id = 5,
                       user_id = 5))
Inst.append(Instrument(name = "Kick Drum",
                       description = "A large, resonating drum played with a foot pedal.",
                       picture = "http://blog.discmakers.com/wp-content/uploads/2012/09/01_BassDrum-292x300.jpg",
                       price = 199,
                       category_id = 5,
                       user_id = 5))
Inst.append(Instrument(name = "Cymbal",
                       description = "A thin, round, metal plate which rings when struck.",
                       picture = "http://www.rpmusic.ca/wp-content/uploads/2014/07/20-Rock-Ride.jpg",
                       price = 49,
                       category_id = 5,
                       user_id = 5))
Inst.append(Instrument(name = "Timpani",
                       description = "A large, kettle-shaped drum with only one head.",
                       picture = "http://s2.lonestarpercussion.com/resize/images/Musser/Adams-P2FI20-full.jpg",
                       price = 399,
                       category_id = 5,
                       user_id = 5))

for inst in Inst:
    session.add(inst)
session.commit()


# Inst.append(Instrument(name = "Sousaphone",
#                        description = "Goes blat.",
#                        picture = "http://www.1800usaband.com/uploads/images/23502.jpg",
#                        price = 1499,
#                        category_id = 2,
#                        user_id = 0))



print "added catalog items!"