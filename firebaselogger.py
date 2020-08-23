
# ===============================================


def LogTime(rfid_id, db):
    from datetime import datetime
    from datetime import date
    now = datetime.now()
    time = now.strftime("%H%M")

    AuthKey = rfid_id

    user_info = ''

    # Log the date
    data = {
        u'Time_In': int(time)
    }

    query = db.collection(u'employees').where(
        u'employeeId', u'==', AuthKey).stream()

    queryLength = db.collection(u'employees').where(
        u'employeeId', u'==', AuthKey).get()

    for employees in query:
        if len(queryLength) == 0:
            print("error")
        else:
            employee_id = employees.id
            db.collection(u'employees').document(employee_id).collection(
                u'Dates_In').document(str(date.today())).set(data)
            print('Successful.')

    # Now set the date time to that employees "date section"
#LogTime("sahil123")