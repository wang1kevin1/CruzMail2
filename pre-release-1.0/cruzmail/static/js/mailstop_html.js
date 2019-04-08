var myModel = {
  name: "Who's Ashley",
  test: '',
  index: 0,
  allTrue: false,

  new_mailstop: '',
  new_ms_name: '',
  new_ms_route: '',
  new_ms_route_order: '',
  Info: [],
  currentView: -1,
  newMailstopView: false,
};

var myViewModel = new Vue({
  el: '#mailstop_view',
  delimiters: ['${', '}'],
  data: myModel,
  methods: {
    change_to_true: changes_to_true = function () {
      var allTrue = !myViewModel.allTrue;
      for (var key in myViewModel.Info)
        myViewModel.Info[key].isActive = allTrue;
    },
    addMailstop: addMailstops = function () {
      $.ajax({
        type: "POST",
        url: '/add_mailstop',
        data: {
          "ms_id": myViewModel.new_mailstop,
          "ms_name": myViewModel.new_ms_name,
          "ms_route": myViewModel.new_ms_route,
          "ms_route_order": myViewModel.new_ms_route_order,
          "ms_status": myViewModel.new_ms_status
        },
        dataType: 'json',
        success: function no(response) {
        },
        error: function (response) {
          console.log("invalid inputs\n");
        }
      });

    },
    activateMailstop: activateMailstops = function () {
      for (var key in myViewModel.Info)
        if (myViewModel.Info[key].isActive)
          $.ajax({
            type: "POST",
            url: '/activate_mailstop',
            data: {
              "mailstop": myViewModel.Info[key].mailstop
            },
            dataType: 'json',
            success: function no(response) {
            },
            error: function (response) {
              console.log("invalid inputs\n");
            }
          });
    },

    deactivateMailstop: deactivateMailstops = function () {
      for (var key in myViewModel.Info)
        if (myViewModel.Info[key].isActive)
          $.ajax({
            type: "POST",
            url: '/deactivate_mailstop',
            data: {
              "mailstop": myViewModel.Info[key].mailstop
            },
            dataType: 'json',
            success: function no(response) {
            },
            error: function (response) {
              console.log("invalid inputs\n");
            }
          });
    },

    updateMailstop: updateMailstops = function () {
      var objHold = myViewModel.Info[myViewModel.currentView];
      console.log(objHold);
      $.ajax({
        type: "POST",
        url: '/update_mailstop',
        data: {
          "ms_id": objHold.mailstop,
          "ms_name": objHold.ms_name,
          "ms_route": objHold.ms_route,
          "ms_route_order": objHold.ms_route_order,
          "ms_status": objHold.ms_status
        },
        dataType: 'json',
        success: function no(response) {
        },
        error: function (response) {
          console.log("invalid inputs\n");
        }
      });
    },
    queryMailstop: queryMailstops = function () {
      myViewModel.allTrue = false;
      myViewModel.currentView = -1;

      $.ajax({
        type: "POST",
        url: '/query_mailstop',
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
              mailstop: objHold.mailstop,
              ms_name: objHold.ms_name,
              ms_route: objHold.ms_route,
              ms_route_order: objHold.ms_route_order,
              ms_status: objHold.ms_status,
              isActive: false,
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
    }

  }

});
myViewModel.queryMailstop();