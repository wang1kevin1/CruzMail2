var myModel = {
  name: "Who's Ashley",
  test: '',
  index: 0,
  
  //true if the general checkbox is checked
  allTrue: false,

  // stores the information for a new person if needed
  new_person: '',
  new_ppl_email: '',
  new_ppl_status: '',
  new_mailstop: '',
  
  //stores the info for all the people
  Info: [],

  //checks if extra data wants to be displayed
  // -1: no person displays extra data
  //positive number: p[erson] of the specific index displays extra data
  currentView: -1,

  //checks if the new person overlay is to be displayed
  newPersonView: false,

  //checks if the import overlay is to be displayed
  newImportView: false,
};

var myViewModel = new Vue({
  el: '#person_view',
  delimiters: ['${', '}'],
  data: myModel,
  methods: {
    change_to_true: changes_to_true = function () {
      var allTrue = !myViewModel.allTrue;
      for (var key in myViewModel.Info)
        myViewModel.Info[key].isAvailable = allTrue;
    },
    addPerson: addPeople = function () {
      $.ajax({
        type: "POST",
        url: '/add_person',
        data: {
          "ppl_name": myViewModel.new_person,
          "ppl_email": myViewModel.new_ppl_email,
          "ppl_status": myViewModel.new_ppl_status,
          "mailstop": myViewModel.new_mailstop
        },
        dataType: 'json',
        success: function no(response) {
        },
        error: function (response) {
          console.log("invalid inputs\n");
        }
      });

    },

    awayPerson: awayPeople = function () {
      for (var key in myViewModel.Info)
        if (myViewModel.Info[key].isAvailable)
          $.ajax({
            type: "POST",
            url: '/away_person',
            data: {
              "name": myViewModel.Info[key].name
            },
            dataType: 'json',
            success: function no(response) {
            },
            error: function (response) {
              console.log("invalid inputs\n");
            }
          });
    },

    updatePerson: updatePeople = function () {
      var objHold = myViewModel.Info[myViewModel.currentView];
      console.log(objHold);
      $.ajax({
        type: "POST",
        url: '/update_person',
        data: {
          "ppl_name": objHold.name,
          "ppl_email": objHold.ppl_email,
          "ppl_status": objHold.ppl_status,
          "mailstop": objHold.mailstop
        },
        dataType: 'json',
        success: function no(response) {
        },
        error: function (response) {
          console.log("invalid inputs\n");
        }
      });
    },

    queryPerson: queryPeople = function () {
      myViewModel.allTrue = false;
      myViewModel.currentView = -1;

      $.ajax({
        type: "POST",
        url: '/query_person',
        data: {
          "search": myViewModel.test,
          "index": myViewModel.index * 10
        },
        dataType: 'json',
        success: function good(response) {
          console.log(response.params);
          myViewModel.Info = [];
          var index = 0;
          var objHold;
          for (var key in response.params) {
            objHold = response.params[key]
            myViewModel.Info.push({
              name: objHold.name,
              ppl_email: objHold.ppl_email,
              ppl_status: objHold.ppl_status,
              mailstop: objHold.mailstop,
              isAvailable: false,
              index: index
            });
            index++;
            //console.log(response.params[key]);
          }
        },
        error: function (response) {
          console.log("invalid inputs\n");
        }
      });
    },

  }

});
myViewModel.queryPerson();