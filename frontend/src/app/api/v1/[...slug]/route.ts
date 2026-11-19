import { NextRequest, NextResponse } from "next/server";

// Backend base URL; override with BACKEND_URL (e.g. in Docker or production).
const BACKEND_URL = (process.env.BACKEND_URL || "http://127.0.0.1:8000").replace(/\/+$/, "");

type Ctx = { params: Promise<{ slug: string[] }> };

export async function GET(request: NextRequest, { params }: Ctx) {
  return proxyRequest(request, params);
}

export async function POST(request: NextRequest, { params }: Ctx) {
  return proxyRequest(request, params);
}

async function proxyRequest(request: NextRequest, params: Promise<{ slug: string[] }>) {
  const path = (await params).slug.map(encodeURIComponent).join("/");
  const backendUrl = `${BACKEND_URL}/api/v1/${path}`;
  const searchParams = request.nextUrl.searchParams.toString();
  const url = searchParams ? `${backendUrl}?${searchParams}` : backendUrl;

  let body: unknown;
  if (request.method === "POST") {
    try {
      body = await request.json();
    } catch {
      return NextResponse.json({ success: false, error: "Invalid JSON body" }, { status: 400 });
    }
  }

  try {
    const response = await fetch(url, {
      method: request.method,
      headers: {
        "Content-Type": "application/json",
      },
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });

    const text = await response.text();
    let data: unknown;
    try {
      data = text ? JSON.parse(text) : {};
    } catch {
      data = { success: false, error: text.slice(0, 200) || "Non-JSON response from backend" };
    }
    return NextResponse.json(data, { status: response.status });
  } catch (error) {
    console.error("Proxy Error:", error);
    const message = error instanceof Error ? error.message : "Backend unreachable";
    // 502: the upstream backend could not be reached.
    return NextResponse.json({ success: false, error: message }, { status: 502 });
  }
}
