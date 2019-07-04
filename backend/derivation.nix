{ python37, python37Packages }:
let
  pyshark = python37.pkgs.buildPythonPackage rec {
    pname = "pyshark";
    version = "0.4.2.3";

    src = python37.pkgs.fetchPypi {
      inherit pname version;
      sha256 = "0g0w55vwvig45lij2amhyc032p15f37c7h6qjf3wpz7lp7qin8kw";
    };

    propagatedBuildInputs = with python37Packages; [ py pytest mock Logbook lxml ];

    doCheck = false;
  };
in 
  python37Packages.buildPythonApplication rec {
    pname = "flower-backend";
    version = "1.0";

    src = ./.;
    propagatedBuildInputs = [ python37Packages.flask-cors python37Packages.flask python37Packages.pymongo python37Packages.waitress pyshark ];

    doCheck = false;
  }

