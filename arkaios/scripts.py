# script that is used to update years to the next year. be careful though. this cannot be undone.

import psycopg2

connection = psycopg2.connect(
    database='piperdb',
    user='phil',
    password='3YToxjG2hj3wYoWKc84a2AYYEBiiABTa',
    host='piper.phizzle.space',
    port=5432
)


cursor = connection.cursor()

get_attendees_query = "SELECT id, first_name, last_name, email, year FROM arkaios_attendee"
cursor.execute(get_attendees_query)
all_attendees = cursor.fetchall()

update_query = "UPDATE arkaios_attendee SET year=%s WHERE id=%s"

for attendee in all_attendees:
    print(attendee)

    if attendee[4] == 'freshman':
        new_year = 'sophomore'
    elif attendee[4] == 'sophomore':
        new_year = 'junior'
    elif attendee[4] == 'junior':
        new_year = 'senior'
    elif attendee[4] == 'senior':
        new_year = 'other'
    else:
        new_year = attendee[4]

    # print('%s -> %s' % (attendee[4], new_year))
    # cursor.execute(update_query, (new_year, attendee[0],))

# connection.commit()
