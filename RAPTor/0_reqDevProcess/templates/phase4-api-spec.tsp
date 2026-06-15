// ============================================================
// API 規格模板 (TypeSpec)
// ============================================================
// 階段: Phase 4 - 規格制定
// 目的: 定義 REST API 規格
// 參考: https://typespec.io/
// ============================================================

import "@typespec/http";
import "@typespec/rest";
import "@typespec/openapi3";

using TypeSpec.Http;
using TypeSpec.Rest;

@service({
  title: "[API 名稱]",
  version: "1.0.0",
})
namespace MyAPI;

// ============================================================
// Models (資料模型)
// ============================================================

model User {
  id: string;
  email: string;
  name: string;
  createdAt: utcDateTime;
}

model CreateUserRequest {
  email: string;
  name: string;
  password: string;
}

model ErrorResponse {
  code: string;
  message: string;
  details?: string;
}

// ============================================================
// Endpoints (API 端點)
// ============================================================
// 注意: @useAuth 裝飾器的權限 ID 必須對應 haARM 的 permission.id
// 參見: phase2-access-control.haarm.yaml
// ============================================================

@route("/users")
interface Users {
  @get
  @useAuth("user_read")            // ← haARM permission.id
  @summary("列出所有使用者")
  list(
    @query page?: int32,
    @query pageSize?: int32,
  ): {
    @statusCode statusCode: 200;
    @body body: {
      data: User[];
      total: int32;
    };
  };

  @post
  @useAuth("user_write")           // ← haARM permission.id
  @summary("建立使用者")
  create(@body request: CreateUserRequest): {
    @statusCode statusCode: 201;
    @body body: User;
  } | {
    @statusCode statusCode: 400;
    @body body: ErrorResponse;
  };

  @get
  @useAuth("user_read")            // ← haARM permission.id
  @summary("取得使用者詳情")
  getById(@path userId: string): {
    @statusCode statusCode: 200;
    @body body: User;
  } | {
    @statusCode statusCode: 404;
    @body body: ErrorResponse;
  };
}
