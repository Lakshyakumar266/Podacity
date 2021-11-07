function convert(val) {
	var s = ["", "k", "m", "b", "t"];
	var sNum = Math.floor(("" + val).length / 3);
	var sVal = parseFloat(
		(sNum != 0 ? val / Math.pow(1000, sNum) : val).toPrecision(2)
	);
	if (sVal % 1 != 0) {
		sVal = sVal.toFixed(1);
	}
	return sVal + s[sNum];
}
