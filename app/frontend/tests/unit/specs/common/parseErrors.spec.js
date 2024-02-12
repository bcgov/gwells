import parseErrors from "@/common/helpers/parseErrors";

const randomObject = {
  location: "Geography Object",
  elevation: 1500,
  terrains: ["Mountain", "Valley", "Plains"],
  bodiesOfWater: {
    rivers: ["Nile", "Amazon"],
    lakes: ["Baikal", "Victoria"],
    oceans: {
      pacific: {
        depth: 10911,
        islands: ["Hawaii", "Fiji"],
      },
      atlantic: {
        depth: 8480,
        islands: ["Azores", "Bahamas"],
      },
    },
  },
  wildlife: [
    {
      species: "Tiger",
      habitat: "Jungle",
      conservationStatus: "Endangered",
    },
    {
      species: "Eagle",
      habitat: "Mountains",
      conservationStatus: "Least Concern",
    },
  ],
  climate: {
    temperature: {
      average: 20,
      extremes: {
        highest: 40,
        lowest: -10,
      },
    },
    precipitation: {
      rainySeason: true,
      averageRainfall: 800,
    },
  },
};

const expectation = [
  "Location",
  "Elevation",
  "Terrains - Mountain",
  "BodiesOfWater - Rivers - Nile",
  "BodiesOfWater - Lakes - Baikal",
  "BodiesOfWater - Oceans - Pacific - Depth",
  "BodiesOfWater - Oceans - Pacific - Islands - Hawaii",
  "BodiesOfWater - Oceans - Atlantic - Depth",
  "BodiesOfWater - Oceans - Atlantic - Islands - Azores",
  "Wildlife - Habitat",
  "Wildlife - Habitat",
  "Wildlife - Habitat",
  "Wildlife - Habitat",
  "Climate - Temperature - Average",
  "Climate - Temperature - Extremes - Highest",
  "Climate - Temperature - Extremes - Lowest",
  "Climate - Temperature - Extremes - Lowest",
  "Climate - Precipitation - RainySeason",
  "Climate - Precipitation - AverageRainfall",
];

describe('parseErrors.js', () => {
  it('tests functionality', () => {
    const response = parseErrors(randomObject)
    expect(response).toEqual(expectation)
  })
})
