const ordinalRules = new Intl.PluralRules("en", { type: "ordinal" });
const suffixes = { one: "st", two: "nd", few: "rd", other: "th" } as const;

const dateFormat = new Intl.DateTimeFormat("en-US")

export function formatRank(num: number): string {
  return `${num}${suffixes[ordinalRules.select(num) as keyof typeof suffixes]}`;
};

export function formatDate(date: string): string {
  return dateFormat.format(new Date(date));
}
