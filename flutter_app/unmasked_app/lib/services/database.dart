import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:unmasked/models/employee.dart';
import 'package:unmasked/models/employee.dart';
import 'package:unmasked/models/user.dart';

class DatabaseService {
  //connecting with firestore
  //collection reference
  final String uid;

  DatabaseService({this.uid});

  final CollectionReference employeeCollection = Firestore.instance.collection('employees');


  Future updateUserData(String employeeId, String name, String email, String phoneNumber, String image) async {
    return await employeeCollection.document(uid).setData({
      'employeeId': employeeId,
      'name': name,
      'email': email,
      'phoneNumber': phoneNumber,
      'image': image
    });
  }

  //employee list from snapshot
  List<Employee> _employeeListFromSnapshot(QuerySnapshot snapshot){
    return snapshot.documents.map((doc){
      return Employee(
        employeeId: doc.data['employeeId'] ?? '',
        name: doc.data['name'] ?? '',
        phoneNumber: doc.data['phoneNumber'] ?? '',
        email:doc.data['email'] ?? '',
        image: doc.data['image'] ?? '',
      );
    }).toList();
  }

  //userData from snapshot
  UserData _userDataFromSnapshot(DocumentSnapshot snapshot) {
    return UserData(
      uid: uid,
      employeeId:snapshot.data['employeeId'],
      name:snapshot.data['name'],
      email:snapshot.data['email'],
      phoneNumber:snapshot.data['phoneNumber'],
      image:snapshot.data['image'],

    );
  }

//get employees stream

  Stream<List<Employee>> get employees {
    return employeeCollection.snapshots()
    .map(_employeeListFromSnapshot);
  }

  //get user doc stream
  Stream<UserData> get userData{
    return employeeCollection.document(uid).snapshots()
        .map(_userDataFromSnapshot);
  }
}