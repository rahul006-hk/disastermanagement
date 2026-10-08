import axios from "axios";
import type {
  Zone, Warehouse, Hospital, Shelter, Vehicle, Road,
  ActionPlanResult, EvaluationMetrics
} from "../types/api";

const API_BASE_URL = "http://localhost:8000/api";

export const api = {
  getZones: async (): Promise<Zone[]> => {
    const res = await axios.get(`${API_BASE_URL}/zones`);
    return res.data;
  },
  getWarehouses: async (): Promise<Warehouse[]> => {
    const res = await axios.get(`${API_BASE_URL}/resources`);
    return res.data;
  },
  getHospitals: async (): Promise<Hospital[]> => {
    const res = await axios.get(`${API_BASE_URL}/hospitals`);
    return res.data;
  },
  getShelters: async (): Promise<Shelter[]> => {
    const res = await axios.get(`${API_BASE_URL}/shelters`);
    return res.data;
  },
  getVehicles: async (): Promise<Vehicle[]> => {
    const res = await axios.get(`${API_BASE_URL}/vehicles`);
    return res.data;
  },
  getRoads: async (): Promise<Road[]> => {
    const res = await axios.get(`${API_BASE_URL}/roads`);
    return res.data;
  },
  toggleRoadBlockage: async (roadId: string, isBlocked: boolean): Promise<Road> => {
    const res = await axios.patch(`${API_BASE_URL}/roads/${roadId}`, { is_blocked: isBlocked });
    return res.data;
  },
  simulateScenario: async (ticks: number = 10): Promise<any> => {
    const res = await axios.post(`${API_BASE_URL}/scenarios/simulate?ticks=${ticks}`);
    return res.data;
  },
  generateActionPlan: async (): Promise<ActionPlanResult> => {
    const res = await axios.post(`${API_BASE_URL}/planning/generate`);
    return res.data;
  },
  runWhatIf: async (payload: any): Promise<any> => {
    const res = await axios.post(`${API_BASE_URL}/planning/what-if`, payload);
    return res.data;
  },
  getEvaluationMetrics: async (): Promise<EvaluationMetrics[]> => {
    const res = await axios.get(`${API_BASE_URL}/planning/evaluation`);
    return res.data;
  }
};
