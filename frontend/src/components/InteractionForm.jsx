import { useDispatch, useSelector } from "react-redux";
import { updateField } from "../redux/interactionSlice";

export default function InteractionForm() {
  const dispatch = useDispatch();
  const form = useSelector((state) => state.interaction);

  const handleChange = (e) => {
    const { name, value } = e.target;

    dispatch(
      updateField({
        field: name,
        value,
      })
    );
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg p-6 h-fit">

      <h2 className="text-3xl font-bold mb-6">
        Interaction Details
      </h2>

      <div className="space-y-5">

        {/* HCP Name */}
        <input
          type="text"
          name="hcpName"
          value={form.hcpName}
          onChange={handleChange}
          placeholder="HCP Name"
          className="w-full border rounded-xl p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        {/* Interaction Type */}
        <select
          name="interactionType"
          value={form.interactionType}
          onChange={handleChange}
          className="w-full border rounded-xl p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="Meeting">Meeting</option>
          <option value="Call">Call</option>
          <option value="Email">Email</option>
        </select>

        {/* Date */}
        <input
          type="date"
          name="date"
          value={form.date}
          onChange={handleChange}
          className="w-full border rounded-xl p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        {/* Time */}
        <input
          type="time"
          name="time"
          value={form.time}
          onChange={handleChange}
          className="w-full border rounded-xl p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        {/* Attendees */}
        <input
          type="text"
          name="attendees"
          value={form.attendees}
          onChange={handleChange}
          placeholder="Attendees"
          className="w-full border rounded-xl p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        {/* Topics */}
        <textarea
          rows={4}
          name="topics"
          value={form.topics}
          onChange={handleChange}
          placeholder="Topics Discussed"
          className="w-full border rounded-xl p-3 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        {/* Materials Shared */}
        <input
          type="text"
          name="materials"
          value={form.materials}
          onChange={handleChange}
          placeholder="Materials Shared"
          className="w-full border rounded-xl p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        {/* Samples Distributed */}
        <input
          type="text"
          name="samples"
          value={form.samples}
          onChange={handleChange}
          placeholder="Samples Distributed"
          className="w-full border rounded-xl p-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        {/* Sentiment */}
        <div>

          <label className="block text-sm font-semibold text-gray-700 mb-3">
            Overall HCP Sentiment
          </label>

          <div className="flex gap-8">

            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                name="sentiment"
                value="Positive"
                checked={form.sentiment === "Positive"}
                onChange={handleChange}
              />
              Positive
            </label>

            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                name="sentiment"
                value="Neutral"
                checked={form.sentiment === "Neutral"}
                onChange={handleChange}
              />
              Neutral
            </label>

            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="radio"
                name="sentiment"
                value="Negative"
                checked={form.sentiment === "Negative"}
                onChange={handleChange}
              />
              Negative
            </label>

          </div>

        </div>

        {/* Outcome */}
        <textarea
          rows={3}
          name="outcome"
          value={form.outcome}
          onChange={handleChange}
          placeholder="Outcome"
          className="w-full border rounded-xl p-3 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        {/* Follow Up */}
        <textarea
          rows={3}
          name="followUp"
          value={form.followUp}
          onChange={handleChange}
          placeholder="Follow-up Actions"
          className="w-full border rounded-xl p-3 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

      </div>

    </div>
  );
}