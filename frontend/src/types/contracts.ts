export type HealthStatus = {
  status: "ok";
  service: string;
  storage: string;
};

export type CaseCreate = {
  text: string;
  language: string;
  photo_urls: string[];
  block: string;
  floor: string | null;
  stairwell: string | null;
  zone_id: string | null;
};

export type CaseRecord = CaseCreate & {
  id: string;
  translation: string | null;
  created_at: string;
  category: "nuisance" | "welfare" | "unclassified";
  priority: number;
  root_cause: string | null;
  status: "new" | "in_review" | "closed" | "archived";
};
