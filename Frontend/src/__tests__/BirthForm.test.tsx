import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { BirthForm } from "../components/BirthForm";
import { DEFAULT_BIRTH_INPUT } from "../types";

describe("BirthForm", () => {
  it("shows a validation error and does not submit when required fields are empty", () => {
    const onSubmit = vi.fn();
    render(
      <BirthForm value={DEFAULT_BIRTH_INPUT} onChange={() => {}} onSubmit={onSubmit} submitting={false} />,
    );
    fireEvent.click(screen.getByRole("button", { name: /run consultation/i }));
    expect(screen.getByRole("alert")).toHaveTextContent(/Required/);
    expect(onSubmit).not.toHaveBeenCalled();
  });

  it("submits the exact value the user typed, without transforming it", () => {
    const onSubmit = vi.fn();
    const value = {
      ...DEFAULT_BIRTH_INPUT,
      date: "1987-03-14",
      time: "04:22",
      timezone: "Asia/Kolkata",
      latitude: 10.787,
      longitude: 79.1378,
    };
    render(<BirthForm value={value} onChange={() => {}} onSubmit={onSubmit} submitting={false} />);
    fireEvent.click(screen.getByRole("button", { name: /run consultation/i }));
    expect(onSubmit).toHaveBeenCalledWith(value);
  });

  it("disables the submit button while submitting", () => {
    render(
      <BirthForm value={DEFAULT_BIRTH_INPUT} onChange={() => {}} onSubmit={() => {}} submitting />,
    );
    expect(screen.getByRole("button", { name: /running consultation/i })).toBeDisabled();
  });

  it("flags an out-of-range latitude without silently correcting it", () => {
    const onSubmit = vi.fn();
    const value = {
      ...DEFAULT_BIRTH_INPUT,
      date: "1987-03-14",
      time: "04:22",
      timezone: "Asia/Kolkata",
      latitude: 999,
      longitude: 79.1378,
    };
    render(<BirthForm value={value} onChange={() => {}} onSubmit={onSubmit} submitting={false} />);
    fireEvent.click(screen.getByRole("button", { name: /run consultation/i }));
    expect(screen.getByRole("alert")).toHaveTextContent(/Latitude must be within/);
    expect(onSubmit).not.toHaveBeenCalled();
  });
});
