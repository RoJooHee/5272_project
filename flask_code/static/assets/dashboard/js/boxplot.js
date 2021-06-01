var lon_a = [ 3733.6460311,
3733.6460293,
3733.6460319,
3733.646036,
3733.6460329,
3733.6460295,
3733.6460298,
3733.6460345,
3733.6460406,
3733.6460257,
3733.6460214,
3733.6460288,
3733.6460206,
3733.6460286,
3733.6460248,
3733.6460293,
3733.6460196,
3733.6460234,
3733.6460153,
3733.646014,
3733.6460225,
3733.6460367,
3733.6460342,
3733.6460268,
3733.6460288,
3733.6460286,
3733.6460292,
3733.6460278,
3733.6460257,
3733.6460374,
3733.6460371,
3733.6460321,
3733.6460258,
3733.646027,
3733.6460337,
3733.6460346,
3733.6460373,
3733.6460265,
3733.6460261,
3733.646027,
3733.6460289,
3733.6460357,
3733.6460436,
3733.6460383,
3733.6460334,
3733.6460343,
3733.6460287,
3733.6460297,
3733.6460254,
3733.6460326
]

var lon_b = [
3733.6467077,
3733.646717,
3733.6467061,
3733.6466952,
3733.6466994,
3733.646697,
3733.6466869,
3733.6466608,
3733.6466264,
3733.6466088,
3733.646614,
3733.6466061,
3733.6465729,
3733.6465583,
3733.6465451,
3733.6465178,
3733.6465054,
3733.6464725,
3733.6464387,
3733.6464224,
3733.6463772,
3733.6463486,
3733.6463303,
3733.6463245,
3733.6462939,
3733.6462517,
3733.6462275,
3733.6462224,
3733.6462406,
3733.6462716,
3733.6462804,
3733.6462872,
3733.6462953,
3733.6463019,
3733.6463207,
3733.6463378,
3733.6463366,
3733.6463353,
3733.6463217,
3733.646329,
3733.6463384,
3733.6463373,
3733.6463295,
3733.6463096,
3733.6463099,
3733.6462962,
3733.6462786,
3733.6462745,
3733.6462574,
3733.6462469,
3733.6462478
]

var trace1 = {
  y: lon_a,
  name: '2020-05-23',
  type: 'box'
};

var trace2 = {
  y: lon_b,
  name: '2020-05-24',
  type: 'box'
};

var data = [trace1, trace2];

Plotly.newPlot('box-lan', data);



