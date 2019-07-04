with import <nixpkgs> {};

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
mkShell 
{
  buildInputs = 
  [
    mongodb
    wireshark
    (python37.withPackages (ps: [ ps.flask-cors ps.flask ps.pymongo pyshark ]))
  ];
}
