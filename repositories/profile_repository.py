from typing import Optional, Dict, Any
from config.database import db_config
from logger.logger import info, error, debug
import json


class ProfileRepository:
    """Repository for profile database operations"""
    
    def find_by_user_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Find profile by user_id"""
        info("[ProfileRepository]", "Buscando perfil por user_id", {"userId": user_id})
        
        conn = None
        try:
            conn = db_config.get_connection()
            cursor = conn.cursor()
            
            query = """
                SELECT id, user_id, personal_url, nickname, is_contact_public,
                       mailing_address, biography, organization, country,
                       social_links, created_at, updated_at
                FROM profiles
                WHERE user_id = %s
            """
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()
            
            if not row:
                debug("[ProfileRepository]", "Perfil no encontrado", {"userId": user_id})
                return None
            
            profile = {
                "id": row[0],
                "user_id": row[1],
                "personal_url": row[2],
                "nickname": row[3],
                "is_contact_public": row[4],
                "mailing_address": row[5],
                "biography": row[6],
                "organization": row[7],
                "country": row[8],
                "social_links": row[9] if row[9] else {},
                "created_at": row[10],
                "updated_at": row[11]
            }
            
            info("[ProfileRepository]", "Perfil encontrado", {
                "userId": user_id,
                "profileId": profile["id"]
            })
            
            return profile
            
        except Exception as e:
            error("[ProfileRepository]", "Error buscando perfil", {
                "userId": user_id,
                "error": str(e)
            })
            raise
        finally:
            if conn:
                cursor.close()
                db_config.return_connection(conn)
    
    def update(self, user_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update profile for a user"""
        info("[ProfileRepository]", "Actualizando perfil", {"userId": user_id})
        
        conn = None
        try:
            conn = db_config.get_connection()
            cursor = conn.cursor()
            
            # Build update query dynamically
            fields = []
            values = []
            
            if "personal_url" in update_data:
                fields.append("personal_url = %s")
                values.append(update_data["personal_url"])
            
            if "nickname" in update_data:
                fields.append("nickname = %s")
                values.append(update_data["nickname"])
            
            if "is_contact_public" in update_data:
                fields.append("is_contact_public = %s")
                values.append(update_data["is_contact_public"])
            
            if "mailing_address" in update_data:
                fields.append("mailing_address = %s")
                values.append(update_data["mailing_address"])
            
            if "biography" in update_data:
                fields.append("biography = %s")
                values.append(update_data["biography"])
            
            if "organization" in update_data:
                fields.append("organization = %s")
                values.append(update_data["organization"])
            
            if "country" in update_data:
                fields.append("country = %s")
                values.append(update_data["country"])
            
            if "social_links" in update_data:
                fields.append("social_links = %s::jsonb")
                values.append(json.dumps(update_data["social_links"]))
            
            if not fields:
                raise ValueError("No fields to update")
            
            fields.append("updated_at = CURRENT_TIMESTAMP")
            values.append(user_id)
            
            query = f"""
                UPDATE profiles
                SET {', '.join(fields)}
                WHERE user_id = %s
                RETURNING id, user_id, personal_url, nickname, is_contact_public,
                          mailing_address, biography, organization, country,
                          social_links, created_at, updated_at
            """
            
            cursor.execute(query, values)
            row = cursor.fetchone()
            
            if not row:
                raise ValueError("Profile not found")
            
            conn.commit()
            
            profile = {
                "id": row[0],
                "user_id": row[1],
                "personal_url": row[2],
                "nickname": row[3],
                "is_contact_public": row[4],
                "mailing_address": row[5],
                "biography": row[6],
                "organization": row[7],
                "country": row[8],
                "social_links": row[9] if row[9] else {},
                "created_at": row[10],
                "updated_at": row[11]
            }
            
            info("[ProfileRepository]", "Perfil actualizado exitosamente", {
                "userId": user_id,
                "profileId": profile["id"]
            })
            
            return profile
            
        except Exception as e:
            if conn:
                conn.rollback()
            error("[ProfileRepository]", "Error actualizando perfil", {
                "userId": user_id,
                "error": str(e)
            })
            raise
        finally:
            if conn:
                cursor.close()
                db_config.return_connection(conn)

