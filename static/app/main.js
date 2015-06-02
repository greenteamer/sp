require.config({
  urlArgs: "bust=" + (new Date()).getTime(),
  waitSeconds: 200,
  paths: {
    "jquery": "vendor/jquery/dist/jquery",
    "cookie": "vendor/jquery/dist/jquery.cookie",
    "react": "vendor/react/react",
    "addons": "vendor/react/react-with-addons",
    "bootstrap": "vendor/bootstrap/dist/js/bootstrap",
    "material": "vendor/node_modules/material-ui/<d></d>ist/js/material",
    "ripples": "vendor/bootstrap-material-design/dist/js/ripples",
    "LoginView": "auth/login",
    // "Navigation": "views/navigation",
    // "AddPost": "views/addPostView"
  },
  shim: {
    "bootstrap": {
      "deps": ['jquery']
    },
    "material": {
      "deps": ['ripples', 'bootstrap']
    },
  }
});

require(['LoginView',], function(LoginView) {  
  new LoginView;
});
