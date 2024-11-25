const csv = `location,type,value
USA,POULTRY,50.0713589267626
USA,BEEF,26.7293486139702
USA,PIG,23.302141032229
USA,SHEEP,0.44835471639525`

const data = csv
  .split('\n')
  .slice(1)
  .map((str) => {
    const [location, type, value] = str.split(',');
    return { location, type, value: parseFloat(value).toFixed(1) };
  });

export default data;