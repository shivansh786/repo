
@app.route("/sme/request")
def sme_request_to_ce():
    if "name" not in session:
        return redirect("/")

    if session['category'] != "SME":
        return redirect("/")

    sme = session['hash']

    submitted = utils.db.get_data('requests')
    entp = utils.db.get_data('enterprises')
    cd = {}
    if submitted is not None:
        for i in submitted:
            if submitted[i]['sme'] == sme:
                class_name = "right label label-success" if submitted[i]['accepted'] == 'yes' else "right label label-danger"
                label = "Accepted" if submitted[i]['accepted'] == 'yes' else "Not Accepted"
                name = entp[submitted[i]['ceid']]['name']
                cd[i] = {
                    'class': class_name,
                    'name': name,
                    'label': label
                }
    return render_template('/sme/request.html', data=entp, submitted=cd, name=session['name'])


@app.route("/sme/request/submit", methods=['POST'])
def submit_sme_request():
    sme = session['hash']
    ceid = request.form['sme']
    utils.submit_request(sme, ceid)
    return ''


@app.route("/sme/decision")
def sme_decision():
    if "name" not in session:
        return redirect("/")
    if session['category'] != "SME":
        return redirect("/")

    temp = utils.db.get_data('orders')
    data = {}
    for i in temp:
        if temp[i]['sme_approved'] == 'no' and 'invested' not in temp[i]:
            data[i] = temp[i]
    # print(data)
    return render_template('/sme/order.html', data=data, name=session['name'])


@app.route('/sme/approve', methods=['POST'])
def sme_approve():
    hash_number = request.form['HashCode']
    workingcapital = request.form['WorkingCapital']
    captialdeadline = request.form['CapitalDeadline']
    utils.update_order_sme(hash_number, workingcapital, captialdeadline)
    return "Error"
