import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:unmasked/models/user.dart';
import 'package:unmasked/screens/authenticate/authenticate.dart';
import 'package:unmasked/screens/home/home.dart';

class Wrapper extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final user = Provider.of<User>(context);

    //return either Home or Authenticate widget
    if (user ==null) {
      return Authenticate();
    }else{
      return Home();
    }
  }
}
