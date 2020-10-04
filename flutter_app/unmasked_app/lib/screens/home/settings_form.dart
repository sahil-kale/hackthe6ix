import 'package:flutter/material.dart';
import 'package:unmasked/models/user.dart';
import 'package:unmasked/shared/constants.dart';
import 'package:provider/provider.dart';
import 'package:unmasked/services/database.dart';
import 'package:unmasked/shared/loading.dart';

class SettingsForm extends StatefulWidget {
  @override
  _SettingsFormState createState() => _SettingsFormState();
}

class _SettingsFormState extends State<SettingsForm> {

  final _formKey = GlobalKey<FormState>();

  //form values
  String _currentEmployeeId;
  String _currentName;
  String _currentEmail;
  String _currentPhoneNumber;
  String _currentImage;

  @override
  Widget build(BuildContext context) {
    final user = Provider.of<User>(context);
    return StreamBuilder<UserData>(
      stream: DatabaseService(uid: user.uid).userData,
      builder: (context, snapshot) {//snapshot is a reference to the data coming down the stream
        if(snapshot.hasData){
          UserData userData = snapshot.data;
          return Form(
              key: _formKey,
              child: Column(
                  children: <Widget>[ //DESIGN EMPLOYEE SETTINGS
                    Text(
                      'Update your employee settings',
                      style: TextStyle(fontSize: 18),
                    ),
                    SizedBox(height: 10),
                    TextFormField(
                      initialValue: userData.employeeId,
                      decoration: textInputDecoration,
                      validator: (val) => val.isEmpty ? 'Please enter EmployeeId' : null,
                      onChanged: (val) => setState(() => _currentEmployeeId = val),
                    ),
                    SizedBox(height:10),
                    TextFormField(
                      initialValue: userData.name,
                      decoration: textInputDecoration,
                      validator: (val) => val.isEmpty ? 'Please enter name' : null,
                      onChanged: (val) => setState(() => _currentName = val),
                    ),
                    SizedBox(height:10),
                    TextFormField(
                      initialValue: userData.email,
                      decoration: textInputDecoration,
                      validator: (val) => val.isEmpty ? 'Please enter email' : null,
                      onChanged: (val) => setState(() => _currentEmail = val),
                    ),
                    SizedBox(height:10),
                    TextFormField(
                      initialValue: userData.phoneNumber,
                      decoration: textInputDecoration,
                      validator: (val) => val.isEmpty ? 'Please enter phone number' : null,
                      onChanged: (val) => setState(() => _currentPhoneNumber = val),
                    ),
                    SizedBox(height:20),
                    //button
                    RaisedButton(
                        color: Colors.pink[400],
                        child: Text(
                          'Update',
                          style: TextStyle(color: Colors.white),
                        ),
                        onPressed: () async {
                          print(_currentName);
                        }
                    )
                  ]
              )
          );
        }else{
          return Loading();
        }//do we have data coming down the stream?
      }
    );
  }
}
