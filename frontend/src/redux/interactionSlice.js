import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  hcpName: "",
  interactionType: "Meeting",
  date: "",
  time: "",
  attendees: "",
  topics: "",
  materials: "",
  samples: "",
  sentiment: "Neutral",
  outcome: "",
  followUp: "",
};

const interactionSlice = createSlice({
  name: "interaction",
  initialState,

  reducers: {
    updateField: (state, action) => {
      const { field, value } = action.payload;
      state[field] = value;
    },

    updateMultipleFields: (state, action) => {
      return {
        ...state,
        ...action.payload,
      };
    },

    resetForm: () => initialState,
  },
});

export const {
  updateField,
  updateMultipleFields,
  resetForm,
} = interactionSlice.actions;

export default interactionSlice.reducer;