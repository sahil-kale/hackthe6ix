import 'package:flutter/material.dart';
import 'package:unmasked/models/employee.dart';

class EmployeeTile extends StatelessWidget {

  final Employee employee;
  EmployeeTile({this.employee});

  @override
  Widget build(BuildContext context) { //DESIGN CARD HERE
    return Padding(
      padding: EdgeInsets.only(top: 8.0),
      child: Card(
        margin: EdgeInsets.fromLTRB(20, 6, 20, 0),
        child: ListTile(
          leading: CircleAvatar(
            radius: 25,
            backgroundColor: Colors.brown,
          ),//image in a circle
          title: Text(employee.name),
          subtitle: Text(employee.email)
        )
      )
    );
  }
}
